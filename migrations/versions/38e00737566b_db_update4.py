"""db update4

Revision ID: 38e00737566b
Revises: f4bc0ea3cadc
Create Date: 2022-03-07 11:55:29.663869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e00737566b'
down_revision = 'f4bc0ea3cadc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('pitch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'pitches', ['pitch_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'pitch_id')
    # ### end Alembic commands ###
