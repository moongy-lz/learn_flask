"""'content'

Revision ID: 08886a8613b9
Revises: 8988b6c2f8b8
Create Date: 2021-01-24 10:44:28.854692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08886a8613b9'
down_revision = '8988b6c2f8b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('src', sa.String(length=255), nullable=True),
    sa.Column('p', sa.String(length=1024), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('tag', sa.String(length=16), nullable=True),
    sa.Column('video', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('content')
    # ### end Alembic commands ###