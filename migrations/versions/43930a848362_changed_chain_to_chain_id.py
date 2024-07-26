"""changed_chain-to_chain_id

Revision ID: 43930a848362
Revises: 7f439d30ae6b
Create Date: 2024-07-27 00:26:50.291194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43930a848362'
down_revision: Union[str, None] = '7f439d30ae6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trades', sa.Column('traded_price', sa.Float(), nullable=True))
    op.add_column('trades', sa.Column('chain_id', sa.Integer(), nullable=False))
    op.drop_column('trades', 'chain')
    op.drop_column('trades', 'current_price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trades', sa.Column('current_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('trades', sa.Column('chain', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('trades', 'chain_id')
    op.drop_column('trades', 'traded_price')
    # ### end Alembic commands ###
