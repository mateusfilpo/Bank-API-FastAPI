from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class AccountOut(BaseModel):
    id: int
    holder: str
    account_type: str
    account_number: str
    balance: float
    created_at: AwareDatetime | NaiveDatetime | None
    status: bool
