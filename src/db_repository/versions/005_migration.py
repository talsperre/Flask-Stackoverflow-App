from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
downvotes = Table('downvotes', post_meta,
    Column('vote_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
    Column('comment_id', Integer),
)

upvotes = Table('upvotes', post_meta,
    Column('vote_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
    Column('comment_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['downvotes'].columns['comment_id'].create()
    post_meta.tables['upvotes'].columns['comment_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['downvotes'].columns['comment_id'].drop()
    post_meta.tables['upvotes'].columns['comment_id'].drop()
