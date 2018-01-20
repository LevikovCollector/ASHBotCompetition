from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from template_builder import TemplateForBot
from db_work import get_topic_by_town


class BotASH():
    def __init__(self):
        api_key = '544146061:AAHqkf3obEukKJM-TQ7yHDy_FTYDS_XkPfU'
        updater = Updater(api_key)

        self.bot_templates = TemplateForBot()
        dispacher = updater.dispatcher
        dispacher.add_handler(CommandHandler("start", self.greet_user))
        dispacher.add_handler(CommandHandler("get_act_concurs", self.get_concurs))

        updater.start_polling()
        updater.idle()

    def greet_user(self, bot, update):
        user_chat_id = update.message.chat_id
        user_name = update.effective_user.first_name
        text = self.bot_templates.get_greeting_template(user_name)

        bot.send_message(chat_id=user_chat_id, text=text, parse_mode=ParseMode.HTML)

    def get_concurs(self, bot, update):
        user_chat_id = update.message.chat_id
        print(user_chat_id)
        concurs_massiv = get_topic_by_town('Москва')
        for concurs in concurs_massiv:
            concurs_date = ''
            if concurs.topic_date_end is None:
                concurs_date = concurs.topic_date_start.strftime('%d-%m-%Y')
            else:
                concurs_date = '({}) - ({})'.format(concurs.topic_date_start.strftime('%d-%m-%Y'),
                                                    concurs.topic_date_end.strftime('%d-%m-%Y'))

            html_text = self.bot_templates.get_concurs_info(name=concurs.topic_name,
                                                            con_link=concurs.topic_link,
                                                            date=concurs_date,
                                                            status=concurs.topic_status,
                                                            town=concurs.topic_town)

            bot.send_message(chat_id=user_chat_id, text=html_text, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    bot = BotASH()
