from fastapi import FastAPI, HTTPException
from decimal import Decimal, ROUND_HALF_UP, getcontext
from threading import Lock
from typing import Dict, Any

# money setup 
getcontext().prec = 28
def q(x: Decimal) -> Decimal:
    """Quantize to 2 decimals using HALF_UP (financial)."""
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

app = FastAPI(title="ATM System")

# in-memory data 
ACCOUNTS: Dict[str, Decimal] = {
    "1001": Decimal("250.00"),
    "1002": Decimal("0.00"),
    "1003": Decimal("999.99"),
}
LOCK = Lock() # ensures atomic updates for deposit/withdraw

# helpers 
def validate_account_number(account_number: str):
    if not account_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid account number format")

def parse_amount(payload: Any) -> Decimal:
    """Manual, friendly validation for the request body."""
    if payload is None or not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Missing JSON body")
    if "amount" not in payload:
        raise HTTPException(status_code=400, detail="Missing 'amount' field")

    raw = payload["amount"]
    
    try:
        dec = Decimal(str(raw))
    except Exception:
        raise HTTPException(status_code=400, detail="'amount' must be a number")

    if dec <= Decimal("0"):
        raise HTTPException(status_code=400, detail="'amount' must be > 0")

    return q(dec) 

# endpoints 
# Simple endpoint to verify that the server is alive
@app.get("/health")
def health():
    return {"message": "ok"}

# GET - Return the current balance for a given account
@app.get("/accounts/{account_number}/balance")
def get_balance(account_number: str):
    validate_account_number(account_number)
    if account_number not in ACCOUNTS:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "account_number": account_number,
        "balance": float(q(ACCOUNTS[account_number]))
    }

# POST - Deposit funds into an account
@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: str, payload: dict):
    validate_account_number(account_number)
    if account_number not in ACCOUNTS:
        raise HTTPException(status_code=404, detail="Account not found")
    amount = parse_amount(payload)
    with LOCK:
        new_bal = q(ACCOUNTS[account_number] + amount)
        ACCOUNTS[account_number] = new_bal
    return {
        "message": "Deposit successful",
        "account_number": account_number,
        "amount": float(amount),
        "balance": float(new_bal),
    }

# POST - Withdraw funds from an account
@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: str, payload: dict):
    validate_account_number(account_number)
    if account_number not in ACCOUNTS:
        raise HTTPException(status_code=404, detail="Account not found")
    amount = parse_amount(payload)
    with LOCK:
        cur = ACCOUNTS[account_number]
        if cur < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        new_bal = q(cur - amount)
        ACCOUNTS[account_number] = new_bal
    return {
        "message": "Withdrawal successful",
        "account_number": account_number,
        "amount": float(amount),
        "balance": float(new_bal),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
