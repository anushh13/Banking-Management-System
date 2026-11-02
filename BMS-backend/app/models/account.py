from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum, ForeignKey, text
from app.database.connection import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    account_number = Column(String(30), nullable=False, unique=True)
    account_type = Column(
        Enum("SAVINGS", "CURRENT", "SALARY", "FIXED_DEPOSIT", name="account_type"),
        nullable=False,
    )
    balance = Column(Numeric(15, 2), server_default=text("0.00"))
    available_balance = Column(Numeric(15, 2), server_default=text("0.00"))
    status = Column(
        Enum("ACTIVE", "INACTIVE", "BLOCKED", "CLOSED", name="account_status"),
        server_default=text("'ACTIVE'"),
    )
    opened_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
