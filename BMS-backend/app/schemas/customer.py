from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    # user_id must already exist in the users table.
    user_id: int = Field(gt=0)
    full_name: str = Field(min_length=2, max_length=150)
    mobile: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=150)
    date_of_birth: date | None = None
    address: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    pincode: str | None = Field(default=None, max_length=10)
    employment_type: str | None = Field(default=None, max_length=50)


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    mobile: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=150)
    date_of_birth: date | None = None
    address: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    pincode: str | None = Field(default=None, max_length=10)
    employment_type: str | None = Field(default=None, max_length=50)


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    full_name: str
    mobile: str | None
    email: str | None
    date_of_birth: date | None
    address: str | None
    city: str | None
    state: str | None
    pincode: str | None
    employment_type: str | None
    kyc_status: str | None
    created_at: datetime | None
