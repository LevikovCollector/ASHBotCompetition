from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///concurs_ash.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class TopicInfo(Base):
    __tablename__='TopicInfo'
    id = Column(Integer, primary_key= True)
    topic_name = Column(String(150))
    topic_link = Column(String(350))
    topic_date_start = Column(Date)
    topic_date_end = Column(Date)
    topic_town = Column(String(150))
    topic_status = Column(String(150))
    topic_is_new = Column(Boolean)

    def __init__(self, topic_name=None, topic_link=None, topic_date_start=None, topic_date_end=None, topic_town=None,
                 topic_status=None, topic_is_new=None):
        self.topic_name = topic_name
        self.topic_link = topic_link
        self.topic_date_start = topic_date_start
        self.topic_date_end = topic_date_end
        self.topic_town = topic_town
        self.topic_status = topic_status
        self.topic_is_new = topic_is_new

    def __repr__(self):
        return '<info {} {} {} {} {}>'.format(self.topic_name, self.topic_link, self.topic_date_start,
                                              self.topic_date_end, self.topic_town, self.topic_status,
                                              self.topic_is_new)


if __name__ == "__main__":
    #Создает базу данных
    Base.metadata.create_all(bind=engine)