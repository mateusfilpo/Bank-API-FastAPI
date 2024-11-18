from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class TransactionIn(BaseModel):
    transaction_type: Literal["SAQUE", "DEPOSITO"]
    amount: float
