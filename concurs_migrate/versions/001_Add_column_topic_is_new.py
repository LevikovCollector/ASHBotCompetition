from sqlalchemy import MetaData, Table, Column, Boolean


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(migrate_engine)
    topic_table = Table('TopicInfo', meta, autoload=True)
    topic_is_new = Column('topic_is_new', Boolean())
    topic_is_new.create(topic_table)
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
