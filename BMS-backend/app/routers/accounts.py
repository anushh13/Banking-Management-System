import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.connection import get_db
from app.models.customer import Customer
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountOut

router = APIRouter(prefix="/accounts", tags=["Account Management"])


def generate_account_number() -> str:
    # Demo-format account number. Production systems need an approved number-allocation service.
    return "BMS" + secrets.token_hex(9).upper()


@router.post("/", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    customer = db.get(Customer, payload.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    if customer.kyc_status != "VERIFIED":
        raise HTTPException(status_code=400, detail="Customer KYC must be VERIFIED before account opening.")

    account = Account(
        customer_id=payload.customer_id,
        branch_id=payload.branch_id,
        account_number=generate_account_number(),
        account_type=payload.account_type,
        balance=0,
        available_balance=0,
        status="ACTIVE",
    )
    db.add(account)
    try:
        db.commit()
        db.refresh(account)
        return account
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid branch or account data.")


@router.get("/", response_model=list[AccountOut])
def list_accounts(customer_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Account)
    if customer_id is not None:
        query = query.filter(Account.customer_id == customer_id)
    return query.order_by(Account.id.desc()).limit(200).all()


@router.get("/{account_number}", response_model=AccountOut)
def get_account(account_number: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return account
