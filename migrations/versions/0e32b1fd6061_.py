"""empty message

Revision ID: 0e32b1fd6061
Revises: 
Create Date: 2019-03-21 20:23:59.804895

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e32b1fd6061'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buyer', sa.Column('address', sa.String(length=50), nullable=True))
    op.add_column('buyer', sa.Column('fullname', sa.String(length=50), nullable=True))
    op.add_column('buyer', sa.Column('phone', sa.String(length=50), nullable=True))
    op.add_column('buyer', sa.Column('url_image', sa.String(length=50), nullable=True))
    op.drop_column('buyer', 'contact')
    op.add_column('item', sa.Column('description', sa.String(length=50), nullable=True))
    op.add_column('item', sa.Column('imgurl1', sa.String(length=50), nullable=True))
    op.add_column('item', sa.Column('imgurl2', sa.String(length=50), nullable=True))
    op.add_column('item', sa.Column('imgurl3', sa.String(length=50), nullable=True))
    op.add_column('item', sa.Column('imgurl4', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('description', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('store_name', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('url_image', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('website', sa.String(length=50), nullable=True))
    op.drop_index('username', table_name='user')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', mysql.VARCHAR(length=50), nullable=True))
    op.create_index('username', 'user', ['username'], unique=True)
    op.drop_column('user', 'website')
    op.drop_column('user', 'url_image')
    op.drop_column('user', 'store_name')
    op.drop_column('user', 'phone')
    op.drop_column('user', 'description')
    op.drop_column('item', 'imgurl4')
    op.drop_column('item', 'imgurl3')
    op.drop_column('item', 'imgurl2')
    op.drop_column('item', 'imgurl1')
    op.drop_column('item', 'description')
    op.add_column('buyer', sa.Column('contact', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('buyer', 'url_image')
    op.drop_column('buyer', 'phone')
    op.drop_column('buyer', 'fullname')
    op.drop_column('buyer', 'address')
    # ### end Alembic commands ###