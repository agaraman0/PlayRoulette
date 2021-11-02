"""empty message

Revision ID: e72cef950c0b
Revises: 909ee23b2114
Create Date: 2021-11-01 11:32:19.844396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e72cef950c0b'
down_revision = '909ee23b2114'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dealers', sa.Column('cid', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'dealers', 'casino', ['cid'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dealers', type_='foreignkey')
    op.drop_column('dealers', 'cid')
    # ### end Alembic commands ###
