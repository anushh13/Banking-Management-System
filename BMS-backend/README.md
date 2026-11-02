# BMS FastAPI starter — two modules

Implements:
1. Customer and account management.
2. Deposits, withdrawals, internal transfers and transaction history.

## Setup

1. Keep this project folder alongside your existing BMS backend, or copy these files into it.
2. Activate your Python 3.12 virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create `.env` from `.env.example` and enter your local MySQL password. Do not share or commit `.env`.
5. Confirm MySQL database `bms_ds` exists and that the SQL schema has already been applied.
6. Start the API from the project root:

   `uvicorn app.main:app --reload --host 127.0.0.1 --port 5000`

7. Open `http://127.0.0.1:5000/docs`.

## Important database assumptions

- The SQL file uses `customers.employment_type` (not `employment_status`).
- A matching row must already exist in `users` before creating a customer profile.
- A matching active branch must already exist in `branches` before creating an account.
- Account creation requires customer `kyc_status = VERIFIED`.
- This starter uses the existing tables and does not create or alter tables.

## Initial test sequence

1. Create a user row in `users` through a separately secured admin/user-registration flow.
2. Create a branch row in `branches`.
3. Set the test customer's KYC status to VERIFIED through an authorized KYC workflow.
4. Create a customer profile using its existing `user_id`.
5. Create an account using the customer ID and branch ID.
6. Test deposits, withdrawals and transfers in Swagger.

## Critical limitations

This is a development/demo starter, not a production core-banking system. It has no login/authorization enforcement yet; do not expose it to a network or real customer data. Add authentication, server-side role and ownership checks, MFA, audit logging, idempotency keys, rate limiting, reconciliation and independent security review before deployment.

The current `transactions` table does not have a transfer-group/related-account column or a double-entry GL table. Internal transfer is represented as two transaction rows sharing a common reference prefix. That is not a substitute for a proper double-entry ledger. The SQL schema also stores no immutable journal entries. Do not use this implementation for real funds.
