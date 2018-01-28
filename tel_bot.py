#!/usr/bin/env /mnt/Bot/ASH/ASHBotCompetition/env/bin/python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from template_builder import TemplateForBot
from db_work import (get_topic_by_town, add_user, get_town_by_user, upd_town_by_user, upd_user_last_command,
                     get_user_last_command, exists_user)
from datetime import datetime
import re


def get_bot_token():
    with open('token', 'r', encoding = 'utf-8') as token_bot:
        t_bot = token_bot.read()
    return t_bot


class BotASH():
    def __init__(self):

        updater = Updater(get_bot_token())

        self.bot_templates = TemplateForBot()
        dispacher = updater.dispatcher
        dispacher.add_handler(CommandHandler("start", self.greet_user))
        dispacher.add_handler(CallbackQueryHandler(self.buttons))
        dispacher.add_handler(MessageHandler(Filters.text, self.listen_user))

        updater.start_polling()
        updater.idle()

    def greet_user(self, bot, update):
        keyboard = [[KeyboardButton('Город отслеживания'), KeyboardButton('Текущий город')],
                    [KeyboardButton('Отобразить конкурсы')]]

        reply_markup = ReplyKeyboardMarkup(keyboard, True)

        user_name = update.effective_user.first_name
        text = self.bot_templates.get_greeting_template(user_name)

        update.message.reply_text(text, reply_markup = reply_markup)

    def get_concurs(self, bot, update, user_chat_id):
        user_chat_id = user_chat_id

        concurs_massiv = ''
        user_town_db = get_town_by_user(user_chat_id)
        if user_town_db is None:
            concurs_massiv = get_topic_by_town('all')
        else:
            concurs_massiv = get_topic_by_town(user_town_db)

        if concurs_massiv != []:
            for concurs in concurs_massiv:
                concurs_date = ''

                if concurs.topic_date_start.strftime('%d-%m-%Y') == datetime.today().strftime('%d-%m-%Y'):
                    concurs.topic_name = '{} (сегодня)'.format(concurs.topic_name)
                if concurs.topic_date_end is None:
                    concurs_date = concurs.topic_date_start.strftime('%d-%m-%Y')
                else:
                    concurs_date = '({}) - ({})'.format(concurs.topic_date_start.strftime('%d-%m-%Y'),
                                                        concurs.topic_date_end.strftime('%d-%m-%Y'))

                html_text = self.bot_templates.get_concurs_info(name=concurs.topic_name,
                                                                con_link=concurs.topic_link,
                                                                date=concurs_date,
                                                                status=concurs.topic_status,
                                                                town=concurs.topic_town.capitalize())

                bot.send_message(chat_id=user_chat_id, text=html_text, parse_mode=ParseMode.HTML)

        else:
            bot.send_message(chat_id = user_chat_id, text = 'В указанном городе конкурсов не найдено',
                                 parse_mode = ParseMode.HTML)

    def buttons(self, bot, update):
        query = update.callback_query
        user_chat_id = update.callback_query.from_user.id
        self.last_command = query.data
        if query.data == 'add_city':
            if exists_user(user_chat_id) is None:
                add_user(user_chat_id, None, query.data)
            else:
                upd_user_last_command(user_chat_id, query.data)
            self.show_message(bot, update, user_chat_id)

        if query.data == 'edit_city':
            upd_user_last_command(user_chat_id, query.data)
            self.show_message(bot, update, user_chat_id)

        if query.data == 'del_city':
            upd_user_last_command(user_chat_id, query.data)
            user_town_db = get_town_by_user(user_chat_id)
            if user_town_db is not None:
                upd_town_by_user(user_chat_id, None)
                bot.send_message(chat_id = user_chat_id,
                                 text = 'Город удален!',
                                 parse_mode = ParseMode.HTML)

            else:
                bot.send_message(chat_id = user_chat_id,
                                 text = 'У Вас не установлен город!',
                                 parse_mode = ParseMode.HTML)

    def show_message(self, bot, update, user_chat_id):
        user_chat_id = user_chat_id
        mes_text = self.bot_templates.get_messages_temlpate(self.last_command)
        bot.send_message(chat_id = user_chat_id, text = mes_text,
                         parse_mode = ParseMode.HTML)

    def listen_user(self, bot, update):
        settings_command = ['отобразить конкурсы', 'город отслеживания', 'текущий город']
        user_chat_id = update.message.chat_id
        text_from_user = str(update.message.text).lower().strip()
        choosen_command = get_user_last_command(user_chat_id)
        user_town_db = get_town_by_user(user_chat_id)

        if text_from_user in settings_command:
            if text_from_user == settings_command[0]:
                self.get_concurs(bot, update, user_chat_id)

            elif text_from_user == settings_command[1]:
                keyboard = [[InlineKeyboardButton("Доб. город", callback_data = 'add_city'),
                             InlineKeyboardButton("Изм. город", callback_data = 'edit_city'),
                             InlineKeyboardButton("Уд. город", callback_data = 'del_city')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id = user_chat_id, text = 'Выберите команду', reply_markup = reply_markup)

            elif text_from_user == settings_command[2]:
                if user_town_db is not None:
                    bot.send_message(chat_id = user_chat_id,
                                     text = 'Ваш город: {}'.format(user_town_db.capitalize()),
                                     parse_mode = ParseMode.HTML)
                else:
                    bot.send_message(chat_id = user_chat_id,
                                     text = 'У Вас не установлен город!',
                                     parse_mode = ParseMode.HTML)

        else:
            if choosen_command == 'add_city':
                if user_town_db is None:
                        if self.check_town(bot, text_from_user, user_chat_id):
                            upd_town_by_user(user_chat_id, text_from_user)
                            bot.send_message(chat_id = user_chat_id,
                                             text = 'Ваш город: {} - сохранен'.format(update.message.text),
                                             parse_mode = ParseMode.HTML)
                else:
                    bot.send_message(chat_id = user_chat_id,
                                     text = 'У Вас уже введен город: {}'.format(user_town_db.capitalize()),
                                     parse_mode = ParseMode.HTML)

            if choosen_command == 'edit_city':
                if user_town_db is None:
                    bot.send_message(chat_id = user_chat_id,
                                     text = 'У Вас не установлен город!',
                                     parse_mode = ParseMode.HTML)
                else:
                    if self.check_town(bot, text_from_user, user_chat_id):
                        upd_town_by_user(user_chat_id, text_from_user)
                        bot.send_message(chat_id = user_chat_id,
                                        text = 'Установлен новый город: {}'.format(text_from_user.capitalize()),
                                        parse_mode = ParseMode.HTML)

            if choosen_command is None:
                bot.send_message(chat_id = user_chat_id,
                                 text = 'У Вас не установлен город!',
                                 parse_mode = ParseMode.HTML)

    def check_town(self, bot, town, user_chat_id):
        good_town = True
        template = '\D+'
        m_town= re.match(template, town)

        if len(re.split('[\.,\,\s ;]', town)) != 1:
            bot.send_message(chat_id = user_chat_id, text = 'Введено более одного города',
                         parse_mode = ParseMode.HTML)
            good_town = False

        elif m_town is None:
            bot.send_message(chat_id = user_chat_id, text = 'Город введен неверно. Попробуйте еще раз '
                                                    , parse_mode = ParseMode.HTML)
            good_town = False
        elif len(town) != m_town.span()[1]:
            bot.send_message(chat_id = user_chat_id, text = 'Город введен неверно. Попробуйте еще раз '
                                                            , parse_mode = ParseMode.HTML)
            good_town = False
        return good_town


if __name__ == '__main__':
    bot = BotASH()
