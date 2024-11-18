from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class TransactionOut(BaseModel):
    id: int
    account_id: int
    transaction_type: str
    amount: float
    created_at: AwareDatetime | NaiveDatetime | None
