from typing import Literal

from pydantic import BaseModel


class AccountIn(BaseModel):
    holder: str
    account_type: Literal["CORRENTE", "POUPANÇA"]


class AccountUpdateIn(BaseModel):
    holder: str | None = None
    status: bool | None = None
