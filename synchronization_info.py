from parser_ash import parser_table_topics
from db_work import db_commit, save_topic_info, get_all_links, upd_is_new
from datetime import datetime
from log import add_log_row

STEP = 15
MAX_NUM_PAGE = 135


def update_table_topic_info():

    links_from_db = get_all_links()
    if links_from_db != []:
        # Проходим все страницы в заданом диапазоне
        for num_page in range(0, MAX_NUM_PAGE, STEP):
            topics_massiv = parser_table_topics(num_page)

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

                if save_new_topic:
                    date_start = datetime.strptime(topic['data_start'], '%Y-%m-%d')
                    if topic['data_end'] is not None:
                        date_end = datetime.strptime(topic['data_end'], '%Y-%m-%d')
                    else:
                        date_end = None

                    if date_start >= datetime.today():
                        save_topic_info(name=topic['name'],
                                        new_link=topic['link'],
                                        town=topic['town'],
                                        date_start=date_start,
                                        date_end=date_end,
                                        status=topic['status'])
                        db_commit()
                    add_log_row('Новый топик: {} ({})'.format(topic['name'], topic['link']))
                else:
                    upd_is_new(db_link[0], False)

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
                               town=topic['town'],
                               date_start=date_start,
                               date_end=date_end,
                               status=topic['status'])
               db_commit()

if __name__ == '__main__':
    #initialization_table_topic_info()
    update_table_topic_info()