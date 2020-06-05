"""empty message

Revision ID: 4f33239d3550
Revises: a635a5560e2d
Create Date: 2020-06-05 13:12:47.259134

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f33239d3550'
down_revision = 'a635a5560e2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(length=120), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=120), nullable=True))
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', mysql.VARCHAR(length=120), nullable=True))
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
