from decimal import Decimal
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.transaction import Transaction


def _reference() -> str:
    return "TXN" + uuid4().hex[:24].upper()


def _get_locked_account(db: Session, account_number: str) -> Account:
    account = (
        db.query(Account)
        .filter(Account.account_number == account_number)
        .with_for_update()
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    if account.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Account is not active.")
    return account


def deposit(db: Session, account_number: str, amount: Decimal, channel: str, description: str | None):
    account = _get_locked_account(db, account_number)
    new_balance = Decimal(account.balance or 0) + amount
    account.balance = new_balance
    account.available_balance = Decimal(account.available_balance or 0) + amount

    txn = Transaction(
        transaction_reference=_reference(),
        account_id=account.id,
        transaction_type="DEPOSIT",
        amount=amount,
        balance_after=new_balance,
        description=description or "Cash deposit",
        channel=channel,
        status="SUCCESS",
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def withdraw(db: Session, account_number: str, amount: Decimal, channel: str, description: str | None):
    account = _get_locked_account(db, account_number)
    available = Decimal(account.available_balance or 0)
    if available < amount:
        raise HTTPException(status_code=400, detail="Insufficient available balance.")

    new_balance = Decimal(account.balance or 0) - amount
    account.balance = new_balance
    account.available_balance = available - amount

    txn = Transaction(
        transaction_reference=_reference(),
        account_id=account.id,
        transaction_type="WITHDRAWAL",
        amount=amount,
        balance_after=new_balance,
        description=description or "Cash withdrawal",
        channel=channel,
        status="SUCCESS",
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def transfer(
    db: Session,
    source_number: str,
    destination_number: str,
    amount: Decimal,
    channel: str,
    description: str | None,
):
    if source_number == destination_number:
        raise HTTPException(status_code=400, detail="Source and destination accounts must differ.")

    # Lock accounts in a stable order to reduce deadlock risk.
    numbers = sorted([source_number, destination_number])
    locked = {n: _get_locked_account(db, n) for n in numbers}
    source = locked[source_number]
    destination = locked[destination_number]

    if Decimal(source.available_balance or 0) < amount:
        raise HTTPException(status_code=400, detail="Insufficient available balance.")

    source_new = Decimal(source.balance or 0) - amount
    destination_new = Decimal(destination.balance or 0) + amount
    source.balance = source_new
    source.available_balance = Decimal(source.available_balance or 0) - amount
    destination.balance = destination_new
    destination.available_balance = Decimal(destination.available_balance or 0) + amount

    group_ref = _reference()
    debit = Transaction(
        transaction_reference=group_ref + "D",
        account_id=source.id,
        transaction_type="TRANSFER",
        amount=amount,
        balance_after=source_new,
        description=description or f"Transfer to {destination_number}",
        channel=channel,
        status="SUCCESS",
    )
    credit = Transaction(
        transaction_reference=group_ref + "C",
        account_id=destination.id,
        transaction_type="TRANSFER",
        amount=amount,
        balance_after=destination_new,
        description=f"Transfer from {source_number}",
        channel=channel,
        status="SUCCESS",
    )
    db.add_all([debit, credit])
    db.commit()
    db.refresh(debit)
    return {"transfer_reference": group_ref, "debit": debit, "credit": credit}
