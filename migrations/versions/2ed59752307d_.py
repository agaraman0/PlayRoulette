"""empty message

Revision ID: 2ed59752307d
Revises: 65d3636c6c3f
Create Date: 2021-11-01 21:30:07.340820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ed59752307d'
down_revision = '65d3636c6c3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bets', sa.Column('uid', sa.Integer(), nullable=False))
    op.add_column('bets', sa.Column('gid', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'bets', 'users', ['uid'], ['id'])
    op.create_foreign_key(None, 'bets', 'games', ['gid'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bets', type_='foreignkey')
    op.drop_constraint(None, 'bets', type_='foreignkey')
    op.drop_column('bets', 'gid')
    op.drop_column('bets', 'uid')
    # ### end Alembic commands ###
