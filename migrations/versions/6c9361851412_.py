"""empty message

Revision ID: 6c9361851412
Revises: a0423dea7ab5
Create Date: 2021-11-02 14:09:36.225362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c9361851412'
down_revision = 'a0423dea7ab5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bets', 'balance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bets', sa.Column('balance', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
