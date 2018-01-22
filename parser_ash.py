from bs4 import BeautifulSoup
import requests, re
from log import add_log_row

URL = 'http://hustle-sa.ru/forum/index.php?showforum=6&prune_day=100&sort_by=Z-A&sort_key=title&st'
TEMP_DATA = '\d\d\d\d-\d\d-\d\d'
TEMP_NAME = '\s\D+'
TEMP_DAY_END = '[,/]\d+'


def parser_town_and_status(input_str):
    try:
        template_with_symbol = '[\.\,]'
        template_with_symbol_and_space = '[\.\,\s]'
        pars_res = re.split(template_with_symbol, input_str, 2)
        if len(pars_res) == 3:
            return [pars_res[1], pars_res[-1]]
        else:
            pars_res = re.split(template_with_symbol_and_space, input_str, 2)
            return [pars_res[1], pars_res[-1]]
    except Exception:
        add_log_row('Не дуалось разобрать город и статус конкурса: {}'.format(input_str), 'war')
        return [None, None]


def get_html(step):
    try:
        return requests.get('{}={}'.format(URL, step)).text
    except Exception as e:
        add_log_row(e.args, 'war')


def parser_table_topics(step):
    html_page = get_html(step)
    soup = BeautifulSoup(html_page, "html.parser")
    table_div_with_data = soup.find('div', class_='tableborder')
    table_with_data = table_div_with_data.find('table').find_all('tr')
    all_topics = []

    start_index = 0
    all_rows = len(table_with_data)
    try:
        if step == 0:
            # find string subject
            for index in range(0, all_rows):
                for rows in table_with_data[index].find_all('td'):
                    try:
                        text = rows.find('b').text
                        if text == 'Темы форума':
                            start_index = index
                            break
                    except AttributeError:
                        pass
                if start_index != 0:
                    break
        # work with rows
        for index in range(start_index + 1, all_rows):
            topic = table_with_data[index].find('a')
            topic_link = topic['href']
            topic_data = get_start_end_date(topic.text)
            topic_name = re.findall(TEMP_NAME, topic.text)[-1].strip()
            con_for_town_and_status = parser_town_and_status(table_with_data[index].find('span', class_='desc').text)
            topic_town = con_for_town_and_status[0].strip()
            topic_status = con_for_town_and_status[1].strip()

            if topic_town in ['СПб']:
               topic_town = 'Санкт-Петербург'

            all_topics.append({'link': topic_link,
                               'name': topic_name.replace('-', ' '),
                               'data_start': topic_data[0],
                               'data_end': topic_data[1],
                               'town': topic_town.replace('г.', ''),
                               'status': topic_status})

        return all_topics

    except ValueError as e:
        add_log_row(e.args, 'war')


def get_start_end_date(date_text):
    date_start = None
    date_end = None
    try:
        date_start = re.findall(TEMP_DATA, date_text)[0]
        day_start = date_start.split('-')[-1]
        day_end = re.findall(TEMP_DAY_END, date_text)[0].replace(',', '').replace('/', '')
        date_end = date_start.replace(day_start, day_end)
    except IndexError:
        pass

    return [date_start, date_end]

if __name__ == '__main__':
    print(parser_table_topics(0))