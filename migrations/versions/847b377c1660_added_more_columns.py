"""added more columns

Revision ID: 847b377c1660
Revises: 14aaeec07f8f
Create Date: 2022-03-08 16:45:20.699355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '847b377c1660'
down_revision = '14aaeec07f8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
