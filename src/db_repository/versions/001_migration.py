from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('userId', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR),
    Column('email', VARCHAR),
)

posts = Table('posts', post_meta,
    Column('post_id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

users = Table('users', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].drop()
    post_meta.tables['posts'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].create()
    post_meta.tables['posts'].drop()
    post_meta.tables['users'].drop()
