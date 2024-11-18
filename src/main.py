from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import (
    AccountInactiveError,
    InsufficientBalanceError,
    NegativeAmountError,
    NotFoundAccountError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operações para autenticação",
    },
    {
        "name": "account",
        "description": "Operações para gerir contas.",
    },
    {
        "name": "transaction",
        "description": "Operações para gerir transações",
    },
]

servers = [
    {"url": "http://localhost:8000", "description": "Ambiente de desenvolvimento"},
]


app = FastAPI(
    title="Bank API",
    version="1.0.0",
    summary="API de um banco.",
    description="""
Bank API ajuda você a criar um banco. 🚀

## Accounts

Você será capaz de fazer:

* **Criar contas**.
* **Recuperar contas**.
* **Recuperar contas por ID**.
* **Atualizar contas**.
* **Excluir contas**.

## Transactions

Você será capaz de:

* **Criar transações**.
* **Recuperar transações de uma conta por ID**.
                """,
    openapi_tags=tags_metadata,
    servers=servers,
    redoc_url=None,
    # openapi_url=None, # disable docs
    lifespan=lifespan,
)

app.include_router(auth.router, tags=["auth"])
app.include_router(account.router, tags=["account"])
app.include_router(transaction.router, tags=["transaction"])


@app.exception_handler(NotFoundAccountError)
async def not_found_account_exception_handler(
    request: Request, exc: NotFoundAccountError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(NegativeAmountError)
async def negative_amount_exception_handler(request: Request, exc: NegativeAmountError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance_exception_handler(
    request: Request, exc: InsufficientBalanceError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(AccountInactiveError)
async def insufficient_balance_exception_handler(
    request: Request, exc: AccountInactiveError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
