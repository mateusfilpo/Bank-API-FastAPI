from fastapi import APIRouter, Depends, status

from src.schemas.account import AccountIn, AccountUpdateIn
from src.security import login_required
from src.services.account import AccountService
from src.views.account import AccountOut

router = APIRouter(prefix="/accounts", dependencies=[Depends(login_required)])

service = AccountService()


@router.get("/", response_model=list[AccountOut])
async def read_accounts(
    limit: int = 20,
    skip: int = 0,
):
    return await service.read_all(limit=limit, skip=skip)


@router.get("/{id}", response_model=AccountOut)
async def read_account(id: int):
    return await service.read(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def create_account(account: AccountIn):
    return await service.create(account)


@router.patch("/{id}", response_model=AccountOut)
async def update_account(id: int, account: AccountUpdateIn):
    return await service.update(id=id, account=account)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_account(id: int):
    await service.delete(id)
