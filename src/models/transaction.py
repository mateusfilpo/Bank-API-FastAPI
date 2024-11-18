import sqlalchemy as sa
from sqlalchemy.sql import func

from src.database import metadata

transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("account_id", sa.Integer, nullable=False),
    sa.Column("transaction_type", sa.String(150), nullable=False),
    sa.Column("amount", sa.Double, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=func.now()),
)
