"""init database

Revision ID: a504f33b58db
Revises: 
Create Date: 2025-04-20 13:57:56.797462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a504f33b58db'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('swap_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wallet_address', sa.String(), nullable=True),
    sa.Column('tx_hash', sa.String(), nullable=True),
    sa.Column('token_in', sa.String(), nullable=True),
    sa.Column('token_out', sa.String(), nullable=True),
    sa.Column('amount_in', sa.Float(), nullable=True),
    sa.Column('amount_out', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_swap_transactions_id'), 'swap_transactions', ['id'], unique=False)
    op.create_index(op.f('ix_swap_transactions_tx_hash'), 'swap_transactions', ['tx_hash'], unique=True)
    op.create_index(op.f('ix_swap_transactions_wallet_address'), 'swap_transactions', ['wallet_address'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_swap_transactions_wallet_address'), table_name='swap_transactions')
    op.drop_index(op.f('ix_swap_transactions_tx_hash'), table_name='swap_transactions')
    op.drop_index(op.f('ix_swap_transactions_id'), table_name='swap_transactions')
    op.drop_table('swap_transactions')
    # ### end Alembic commands ###
