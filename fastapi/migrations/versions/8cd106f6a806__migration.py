"""_migration

Revision ID: 8cd106f6a806
Revises: e914f5dc18a0
Create Date: 2024-10-22 17:14:35.245615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cd106f6a806'
down_revision: Union[str, None] = 'e914f5dc18a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'telegram_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'telegram_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
