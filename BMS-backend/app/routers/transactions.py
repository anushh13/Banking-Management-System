from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import MoneyRequest, TransferRequest, TransactionOut
from app.services.transaction_service import deposit, withdraw, transfer

router = APIRouter(prefix="/transactions", tags=["Core Banking Transactions"])


@router.post("/deposit", response_model=TransactionOut)
def make_deposit(account_number: str, payload: MoneyRequest, db: Session = Depends(get_db)):
    try:
        return deposit(db, account_number, payload.amount, payload.channel, payload.description)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Deposit could not be completed.")


@router.post("/withdraw", response_model=TransactionOut)
def make_withdrawal(account_number: str, payload: MoneyRequest, db: Session = Depends(get_db)):
    try:
        return withdraw(db, account_number, payload.amount, payload.channel, payload.description)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Withdrawal could not be completed.")


@router.post("/transfer")
def make_transfer(account_number: str, payload: TransferRequest, db: Session = Depends(get_db)):
    try:
        result = transfer(
            db,
            account_number,
            payload.destination_account_number,
            payload.amount,
            payload.channel,
            payload.description,
        )
        return {
            "message": "Transfer completed.",
            "transfer_reference": result["transfer_reference"],
            "debit": TransactionOut.model_validate(result["debit"]),
            "credit": TransactionOut.model_validate(result["credit"]),
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transfer could not be completed.")


@router.get("/account/{account_number}", response_model=list[TransactionOut])
def account_transaction_history(account_number: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return (
        db.query(Transaction)
        .filter(Transaction.account_id == account.id)
        .order_by(Transaction.transaction_date.desc())
        .limit(200)
        .all()
    )
