import sqlalchemy as sa
from sqlalchemy.sql import func

from src.database import metadata

accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("holder", sa.String(150), nullable=False),
    sa.Column("account_number", sa.String(150), nullable=False, unique=True),
    sa.Column("account_type", sa.String(150), nullable=False),
    sa.Column("balance", sa.Double, nullable=False, server_default="0"),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=func.now()),
    sa.Column("status", sa.Boolean, nullable=False, server_default="true"),
)
