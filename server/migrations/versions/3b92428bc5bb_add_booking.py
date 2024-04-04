"""add booking

Revision ID: 3b92428bc5bb
Revises: 1c2e4cab20ca
Create Date: 2024-04-04 14:11:12.623496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b92428bc5bb'
down_revision = '1c2e4cab20ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('destination', sa.String(), nullable=True),
    sa.Column('flight_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], name=op.f('fk_bookings_customer_id_customers')),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], name=op.f('fk_bookings_flight_id_flights')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    # ### end Alembic commands ###
