"""add relationship

Revision ID: c7ad7898bdf7
Revises: 6eb4f631e547
Create Date: 2023-04-09 15:00:40.562922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ad7898bdf7'
down_revision = '6eb4f631e547'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memos_labels',
    sa.Column('memo_id', sa.Integer(), nullable=False),
    sa.Column('label_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['label_id'], ['label.id'], ),
    sa.ForeignKeyConstraint(['memo_id'], ['memo.id'], ),
    sa.PrimaryKeyConstraint('memo_id', 'label_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memos_labels')
    # ### end Alembic commands ###
