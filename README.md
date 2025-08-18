# 🏦 ATM System API

A simple ATM simulation API built with FastAPI.  
The system supports depositing, withdrawing, and checking balances for in-memory accounts, with proper validation and error handling.  

---
## Features
- Create new accounts
- Deposit & withdraw money
- Check account balance
- Error handling for invalid inputs
- Health check endpoint

## Tech Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Deployment**: Render (Free plan)
- **Testing**: Postman

## Installation:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/atm-system.git
   cd atm-system
    ````

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Server:

Run with:

```bash
uvicorn app:app --reload
```

Default server URL:
 [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger documentation:
 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

ReDoc documentation:
 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Deployment (Render)

This API is deployed on Render (Free plan).

- Live API: `https://atm-system-v85j.onrender.com`
- Health: `https://atm-system-v85j.onrender.com/health`
- Docs (Swagger): `https://atm-system-v85j.onrender.com/docs`

Note about Free plan: the service may go idle when unused.  
The first request after idle can take a few seconds (cold start). Subsequent requests are fast.


 # API Endpoints:
 ## Health check

Method: GET /health
Description: Used to check if the server is running.
Response:

{ "message": "ok" }

 ## Get Balance

Method: GET /accounts/{account_number}/balance
Description: Returns the current balance of the given account.
Path parameter:

account_number → account identifier (string or number).

Success response (200):

{
  "account_number": "1001",
  "balance": 250.0
}

Error cases:

400 → invalid account format

404 → account not found

 ## Deposit

Method: POST /accounts/{account_number}/deposit
Description: Adds funds to an account.
Body:

{ "amount": 50 }


Success response (200):

{
  "message": "Deposit successful",
  "account_number": "1001",
  "amount": 50.0,
  "balance": 300.0
}

Error cases:

400 → invalid body (missing amount, negative or zero value, non-numeric).

404 → account not found.

## Withdraw

Method: POST /accounts/{account_number}/withdraw
Description: Withdraws funds from an account.
Body:

{ "amount": 100 }


Success response (200):

{
  "message": "Withdrawal successful",
  "account_number": "1001",
  "amount": 100.0,
  "balance": 200.0
}

Error cases:

400 → invalid body, missing amount, non-positive value, or insufficient funds.

404 → account not found.

## Testing with Postman

A Postman collection (`atm_system.postman_collection.json`) is included.

How to use:

1. Open **Postman** → Import → Select the JSON file.
2. Ensure the base URL is set to `http://127.0.0.1:8000`.
3. Run the predefined requests (balance, deposit, withdraw, and error cases).

---

## Design Choices:

* **Decimal for money**: Python `Decimal` ensures precise financial calculations, avoiding floating-point errors.
* **Quantization**: All balances are normalized to 2 decimal places with `ROUND_HALF_UP` (typical financial rounding).
* **Thread safety**: Deposits and withdrawals use a global `Lock` to avoid race conditions. Reads (`GET balance`) are lock-free for performance.
* **Manual validation**: Instead of only relying on FastAPI’s built-in validation, custom checks were added for friendlier, clearer error messages.
* **Status codes**:
  * 400 for invalid requests (bad body, invalid amount, insufficient funds).
  * 404 for account not found.

---

## Challenges & Decisions:

- Choosing the stack: I debated whether to use Node.js or Python. Finally picked FastAPI because it’s quick to set up, has async support, and generates nice docs automatically.
- Money precision: At first I used floats, but quickly realized it might cause rounding errors. I switched to Decimal to keep things accurate.
- Error handling: Tried FastAPI’s auto-validation only, but the errors felt too raw. I added manual checks so the API feels clearer and more user-friendly.
- Thread safety: I wasn’t sure whether to lock balance checks too. Decided not to, since they don’t change the state and slight staleness is acceptable.
- Hosting: Considered AWS/Heroku, but for a small project and no budget I’d choose Render as an easy free option.
- I faced a few small challenges: connecting GitHub and working around the free plan limitations (manual deploys, cold starts).  
  Eventually I managed to configure it successfully, and the live link is stable and accessible.


---

## Example Errors:

Invalid account number:

```json
{ "detail": "Invalid account number format" }
```

Account not found:

```json
{ "detail": "Account not found" }
```

Invalid body:

```json
{ "detail": "Missing 'amount' field" }
```

Insufficient funds:

```json
{ "detail": "Insufficient funds" }
```

---

## Future Improvements

* Persistent storage (DB instead of in-memory).
* User accounts & authentication (e.g.,login,JWT).
* Account creation endpoint.
* PUT/DELETE endpoints for updating account metadata
* Improved transaction history tracking.

---
Thanks for checking out this project! 😊  
Hope you enjoyed it  
Roni
