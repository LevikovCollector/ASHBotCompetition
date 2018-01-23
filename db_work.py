from db_ash_conf import TopicInfo, User, db_session
from log import add_log_row
from datetime import datetime


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


def get_topic_id_link_date_s():
    try:
        return db_session.query(TopicInfo.id, TopicInfo.topic_link, TopicInfo.topic_date_start).all()
    except Exception as e:
        add_log_row(e.args, 'war')


def db_commit():
    try:
        db_session.commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def upd_topic(topic_id, name, data_s, data_e, town, status, st_new):
    try:
        old_topic = db_session.query(TopicInfo).get(topic_id)
        old_topic.topic_name = name
        old_topic.topic_date_start = data_s
        old_topic.topic_date_end = data_e
        old_topic.topic_town = town
        old_topic.topic_status = status
        old_topic.topic_is_new = st_new
        db_commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def del_old_topic(topic_id):
    try:
        topic_for_del = db_session.query(TopicInfo).get(topic_id)
        db_session.delete(topic_for_del)
        db_commit()
        add_log_row('Удалена запись: {}'.format(topic_id), 'mes')
    except Exception as e:
        add_log_row(e.args, 'war')


def add_user(user_chat, user_town, last_command):
    try:
        new_user = User(user_chat, user_town, last_command)
        db_session.add(new_user)
        db_commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def get_town_by_user(user_chat):
    try:
        user = User()
        info = user.query.get(user_chat)
        return info.user_town
    except Exception as e:
        add_log_row(e.args, 'war')


def upd_town_by_user(user_chat,  new_town):
    try:
        old_town = db_session.query(User).get(user_chat)
        old_town.user_town = new_town
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


def upd_user_last_command(user_chat, new_command):
    try:
        old_command = db_session.query(User).get(user_chat)
        old_command.user_last_command = new_command
        db_commit()
    except Exception as e:
        add_log_row(e.args, 'war')


def get_user_last_command(user_chat):
    try:
        user = User()
        info = user.query.get(user_chat)
        return info.user_last_command
    except Exception as e:
        add_log_row(e.args, 'war')


def exists_user(user_chat):
    try:
        user = User()
        info = user.query.get(user_chat)
        return info
    except Exception as e:
        add_log_row(e.args, 'war')

if __name__ == '__main__':
    print()
