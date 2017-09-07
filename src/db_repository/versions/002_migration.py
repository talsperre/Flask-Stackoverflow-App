from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('post_id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR),
    Column('timestamp', DATETIME),
    Column('user_roll', INTEGER),
)

answers = Table('answers', post_meta,
    Column('answer_id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('body', Text),
    Column('code', Text),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('question_id', Integer),
)

comments = Table('comments', post_meta,
    Column('comment_id', Integer, primary_key=True, nullable=False),
    Column('body', Text),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
)

questions = Table('questions', post_meta,
    Column('question_id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('body', Text),
    Column('code', Text),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

votes = Table('votes', post_meta,
    Column('vote_id', Integer, primary_key=True, nullable=False),
    Column('vote_type', Integer),
    Column('user_id', Integer),
    Column('question_id', Integer),
    Column('answer_id', Integer),
)

users = Table('users', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('username', String),
    Column('email', String),
    Column('password_hash', String(length=128)),
    Column('reputation', Integer),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].drop()
    post_meta.tables['answers'].create()
    post_meta.tables['comments'].create()
    post_meta.tables['questions'].create()
    post_meta.tables['votes'].create()
    post_meta.tables['users'].columns['last_seen'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].create()
    post_meta.tables['answers'].drop()
    post_meta.tables['comments'].drop()
    post_meta.tables['questions'].drop()
    post_meta.tables['votes'].drop()
    post_meta.tables['users'].columns['last_seen'].drop()
