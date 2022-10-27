"""empty message

Revision ID: 642b87eb8ea5
Revises: bc676413ca3d
Create Date: 2022-10-25 20:57:34.832418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642b87eb8ea5'
down_revision = 'bc676413ca3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pets', sa.Column('description', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pets', 'description')
    # ### end Alembic commands ###