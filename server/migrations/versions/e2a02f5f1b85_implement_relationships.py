"""implement relationships

Revision ID: e2a02f5f1b85
Revises: b609fdb74603
Create Date: 2024-04-09 18:00:49.680642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2a02f5f1b85'
down_revision = 'b609fdb74603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('missions', sa.Column('scientist_id', sa.Integer(), nullable=True))
    op.add_column('missions', sa.Column('planet_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_missions_scientist_id_scientists'), 'missions', 'scientists', ['scientist_id'], ['id'])
    op.create_foreign_key(op.f('fk_missions_planet_id_planets'), 'missions', 'planets', ['planet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_missions_planet_id_planets'), 'missions', type_='foreignkey')
    op.drop_constraint(op.f('fk_missions_scientist_id_scientists'), 'missions', type_='foreignkey')
    op.drop_column('missions', 'planet_id')
    op.drop_column('missions', 'scientist_id')
    # ### end Alembic commands ###
