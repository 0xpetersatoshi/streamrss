"""add rules table

Revision ID: 02e1086149a8
Revises: 
Create Date: 2022-07-24 12:05:46.052524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02e1086149a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pattern', sa.String(), nullable=True),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rules_id'), 'rules', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rules_id'), table_name='rules')
    op.drop_table('rules')
    # ### end Alembic commands ###