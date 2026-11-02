from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum, ForeignKey, text
from app.database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_reference = Column(String(50), nullable=False, unique=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    transaction_type = Column(
        Enum(
            "DEPOSIT", "WITHDRAWAL", "TRANSFER", "PAYMENT",
            "UPI", "NEFT", "RTGS", "IMPS",
            name="transaction_type",
        ),
        nullable=False,
    )
    amount = Column(Numeric(15, 2), nullable=False)
    balance_after = Column(Numeric(15, 2), nullable=False)
    description = Column(String(255))
    channel = Column(
        Enum("BRANCH", "ATM", "ONLINE", "MOBILE", "UPI", name="transaction_channel"),
        server_default=text("'ONLINE'"),
    )
    status = Column(
        Enum("PENDING", "SUCCESS", "FAILED", "REVERSED", name="transaction_status"),
        server_default=text("'PENDING'"),
    )
    transaction_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
