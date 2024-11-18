import random

from databases.interfaces import Record

from src.database import database
from src.exceptions import NotFoundAccountError
from src.models.account import accounts
from src.schemas.account import AccountIn, AccountUpdateIn


class AccountService:
    async def read_all(self, limit: int, skip: int) -> list[Record]:
        query = accounts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def read(self, id: int) -> Record:
        result = await self.__get_by_id(id)
        return {
            "id": result["id"],
            "holder": result["holder"],
            "account_type": result["account_type"],
            "account_number": result["account_number"],
            "balance": float(result["balance"]),
            "created_at": result["created_at"],
            "status": bool(result["status"]),
        }

    async def create(self, account: AccountIn) -> Record:
        while True:
            account_number = self.__create_account_number()
            if not await self.__exists_account_number(account_number):
                break

        command = accounts.insert().values(
            holder=account.holder,
            account_type=account.account_type,
            account_number=account_number,
        )
        result_id = await database.execute(command)

        query = accounts.select().where(accounts.c.id == result_id)
        result = await database.fetch_one(query)

        return {
            "id": result["id"],
            "holder": result["holder"],
            "account_type": result["account_type"],
            "account_number": result["account_number"],
            "balance": float(result["balance"]),
            "created_at": result["created_at"],
            "status": bool(result["status"]),
        }

    async def update(self, id: int, account: AccountUpdateIn) -> Record:
        total = await self.count(id)
        if not total:
            raise NotFoundAccountError()

        data = account.model_dump(exclude_unset=True)
        command = accounts.update().where(accounts.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    async def update_balance(self, id: int, new_balance: float):
        command = (
            accounts.update().where(accounts.c.id == id).values(balance=new_balance)
        )
        await database.execute(command)

    async def delete(self, id: int) -> None:
        total = await self.count(id)
        if not total:
            raise NotFoundAccountError()

        command = accounts.delete().where(accounts.c.id == id)
        await database.execute(command)

    async def count(self, id: int) -> int:
        query = "SELECT COUNT(id) AS total FROM accounts WHERE id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def __get_by_id(self, id: int) -> Record:
        query = accounts.select().where(accounts.c.id == id)
        account = await database.fetch_one(query)
        if not account:
            raise NotFoundAccountError()
        return account

    async def __exists_account_number(self, account_number: str) -> bool:
        query = accounts.select().where(accounts.c.account_number == account_number)
        account = await database.fetch_one(query)
        if not account:
            return False
        return True

    def __create_account_number(self):
        return f"{random.randint(10000000, 99999999)}-{random.randint(0, 9)}"
