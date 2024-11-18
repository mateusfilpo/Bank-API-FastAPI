from databases.interfaces import Record

from src.database import database
from src.exceptions import (
    AccountInactiveError,
    InsufficientBalanceError,
    NegativeAmountError,
)
from src.models.transaction import transactions
from src.schemas.transaction import TransactionIn
from src.services.account import AccountService

account_service = AccountService()


class TransactionService:
    async def read_account_transactions(
        self, id: int, limit: int, skip: int
    ) -> list[Record]:
        query = (
            transactions.select()
            .where(transactions.c.account_id == id)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    async def create_transaction(self, id: int, transaction: TransactionIn) -> Record:
        if transaction.amount < 0:
            raise NegativeAmountError()

        account = await account_service.read(id)

        account_status = account["status"]
        if account_status == False:
            raise AccountInactiveError()

        account_balance = account["balance"]

        if (
            transaction.transaction_type == "SAQUE"
            and transaction.amount > account_balance
        ):
            raise InsufficientBalanceError()

        if transaction.transaction_type == "DEPOSITO":
            account_balance += transaction.amount
        else:
            account_balance -= transaction.amount

        command = transactions.insert().values(
            account_id=id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
        )
        result_id = await database.execute(command)

        await account_service.update_balance(id, account_balance)

        query = transactions.select().where(transactions.c.id == result_id)
        result = await database.fetch_one(query)

        return {
            "id": result["id"],
            "account_id": result["account_id"],
            "transaction_type": result["transaction_type"],
            "amount": float(result["amount"]),
            "created_at": result["created_at"],
        }
