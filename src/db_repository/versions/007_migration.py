from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
questions = Table('questions', post_meta,
    Column('question_id', Integer, primary_key=True, nullable=False),
    Column('title', String),
    Column('body', Text),
    Column('code', Text),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('answered', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['answered'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['answered'].drop()
