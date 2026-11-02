from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


Channel = Literal["BRANCH", "ATM", "ONLINE", "MOBILE", "UPI"]


class MoneyRequest(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=13, decimal_places=2)
    channel: Channel = "ONLINE"
    description: str | None = Field(default=None, max_length=255)


class TransferRequest(MoneyRequest):
    destination_account_number: str = Field(min_length=5, max_length=30)


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_reference: str
    account_id: int
    transaction_type: str
    amount: Decimal
    balance_after: Decimal
    description: str | None
    channel: str | None
    status: str | None
    transaction_date: datetime | None
