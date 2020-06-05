"""empty message

Revision ID: 7d7ecbeae291
Revises: 99f1e15d0f2f
Create Date: 2020-05-25 19:55:43.560581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d7ecbeae291'
down_revision = '99f1e15d0f2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_link')
    # ### end Alembic commands ###