from fastapi import APIRouter, Depends

from src.schemas.transaction import TransactionIn
from src.security import login_required
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut

router = APIRouter(dependencies=[Depends(login_required)])

service = TransactionService()


@router.get("/accounts/{id}/transactions", response_model=list[TransactionOut])
async def read_account_transactions(
    id: int,
    limit: int = 20,
    skip: int = 0,
):
    return await service.read_account_transactions(id=id, limit=limit, skip=skip)


@router.post("/accounts/{id}/transactions", response_model=TransactionOut)
async def create_transaction(id: int, transaction: TransactionIn):
    return await service.create_transaction(id=id, transaction=transaction)
