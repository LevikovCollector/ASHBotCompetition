#!/usr/bin/env /mnt/Bot/ASH/ASHBotCompetition/env/bin/python
from parser_ash import parser_table_topics
from db_work import db_commit, save_topic_info, get_topic_id_link_date_s, upd_topic, del_old_topic
from datetime import datetime
from log import add_log_row

STEP = 15
MAX_NUM_PAGE = 135


def update_table_topic_info():

    links_from_db = get_topic_id_link_date_s()
    if links_from_db != []:
        # Проходим все страницы в заданом диапазоне
        for num_page in range(0, MAX_NUM_PAGE, STEP):
            topics_massiv = parser_table_topics(num_page)
            db_link =[]
            save_new_topic = False
            # Проверяем наличие ссылки в БД
            for topic in topics_massiv:
                topic_sait_id = topic['link'].split('=')[-1]
                for db_link in links_from_db:
                    link_db_id = db_link[1].split('=')[-1]
                    if topic_sait_id != link_db_id:
                        save_new_topic = True
                    else:
                        save_new_topic = False
                        break

                date_start = datetime.strptime(topic['data_start'], '%Y-%m-%d')
                if topic['data_end'] is not None:
                    date_end = datetime.strptime(topic['data_end'], '%Y-%m-%d')
                else:
                    date_end = None
                if save_new_topic:
                    if date_start >= datetime.today():
                        save_topic_info(name=topic['name'],
                                        new_link=topic['link'],
                                        town=topic['town'].lower(),
                                        date_start=date_start,
                                        date_end=date_end,
                                        status=topic['status'])
                        db_commit()
                    add_log_row('Новый топик: {} ({})'.format(topic['name'], topic['link']))
                else:
                    if db_link[2] <= datetime.today().date():
                        del_old_topic(db_link[0])

                    else:
                        upd_topic(topic_id=db_link[0],
                                  name=topic['name'],
                                  town=topic['town'].lower(),
                                  data_s=date_start,
                                  data_e=date_end,
                                  status=topic['status'],
                                  st_new=False)
    else:
        add_log_row('Таблица пустая, запускается инициализация данных')
        initialization_table_topic_info()


def initialization_table_topic_info():
   for num_page in range(0, MAX_NUM_PAGE, STEP):
       topics_massiv = parser_table_topics(num_page)
       for topic in topics_massiv:
           date_start = datetime.strptime(topic['data_start'], '%Y-%m-%d')
           if topic['data_end'] is not None:
              date_end = datetime.strptime(topic['data_end'], '%Y-%m-%d')
           else:
              date_end = None
           if date_start >= datetime.today():
               save_topic_info(name=topic['name'],
                               new_link=topic['link'],
                               town=topic['town'].lower(),
                               date_start=date_start,
                               date_end=date_end,
                               status=topic['status'])
               db_commit()

if __name__ == '__main__':
    update_table_topic_info()