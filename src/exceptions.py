from http import HTTPStatus


class NotFoundAccountError(Exception):
    def __init__(
        self,
        message: str = "Account not found",
        status_code: int = HTTPStatus.NOT_FOUND,
    ) -> None:
        self.message = message
        self.status_code = status_code


class NegativeAmountError(Exception):
    def __init__(
        self,
        message: str = "Amount cannot be negative",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        self.message = message
        self.status_code = status_code


class InsufficientBalanceError(Exception):
    def __init__(
        self,
        message: str = "Insufficient balance",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        self.message = message
        self.status_code = status_code


class AccountInactiveError(Exception):
    def __init__(
        self,
        message: str = "Account is inactive",
        status_code: int = HTTPStatus.FORBIDDEN,
    ) -> None:
        self.message = message
        self.status_code = status_code
