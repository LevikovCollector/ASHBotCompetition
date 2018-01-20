from db_ash_conf import TopicInfo, db_session
from datetime import datetime
from log import add_log_row


def save_topic_info(name, new_link, date_start, date_end, town, status):
    try:
        new_topic = TopicInfo(name, new_link, date_start, date_end, town, status, topic_is_new=True)
        db_session.add(new_topic)
    except Exception as e:
        add_log_row(e.args, 'war')


def get_topic_by_town(town='all'):
    try:
        topic_by_town = TopicInfo()
        if town != 'all':
            return topic_by_town.query.filter(TopicInfo.topic_town == town).order_by(TopicInfo.topic_date_start).all()
        else:
            return topic_by_town.query.order_by(TopicInfo.topic_date_start).all()
    except Exception as e:
        add_log_row(e.args, 'war')


def get_all_links():
    try:
        return db_session.query(TopicInfo.id, TopicInfo.topic_link).all()
    except Exception as e:
        add_log_row(e.args, 'war')


def db_commit():
    try:
        db_session.commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def upd_is_new(topic_id, value):
    try:
        old_topic = db_session.query(TopicInfo).get(topic_id)
        old_topic.topic_is_new = value
        db_commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def get_only_new_topics(town='all'):
    try:
        all_new_topics = TopicInfo()
        if town == 'all':
            return all_new_topics.query.filter(TopicInfo.topic_is_new == 1).\
                order_by(TopicInfo.topic_date_start).all()
        else:
            return all_new_topics.query.filter(TopicInfo.topic_is_new == 1).filter(TopicInfo.topic_town == town).\
                order_by(TopicInfo.topic_date_start).all()

    except Exception as e:
        add_log_row(e.args, 'war')

if __name__ == '__main__':
   links = get_topic_by_town('Москва')
   for link in links:
       print(link.topic_name)

