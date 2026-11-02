from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey, text
from app.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    full_name = Column(String(150), nullable=False)
    mobile = Column(String(20))
    email = Column(String(150))
    date_of_birth = Column(Date)
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    employment_type = Column(String(50))
    kyc_status = Column(
        Enum("PENDING", "VERIFIED", "REJECTED", name="customer_kyc_status"),
        nullable=True,
        server_default=text("'PENDING'"),
    )
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
