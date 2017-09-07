from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
votes = Table('votes', pre_meta,
    Column('vote_id', INTEGER, primary_key=True, nullable=False),
    Column('vote_type', INTEGER),
    Column('user_id', INTEGER),
    Column('question_id', INTEGER),
    Column('answer_id', INTEGER),
)

downvotes = Table('downvotes', post_meta,
    Column('vote_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
)

upvotes = Table('upvotes', post_meta,
    Column('vote_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['votes'].drop()
    post_meta.tables['downvotes'].create()
    post_meta.tables['upvotes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['votes'].create()
    post_meta.tables['downvotes'].drop()
    post_meta.tables['upvotes'].drop()
