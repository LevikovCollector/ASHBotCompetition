from jinja2 import Template


class TemplateForBot():
    def __init__(self):
        self.greeting_template_path = 'templates\greeting.html'
        self.concurs_template_path = 'templates\concurs.html'

    def get_greeting_template(self, name):
        with open(self.greeting_template_path, 'r', encoding='utf-8') as greet_temp:
            html_text = greet_temp.read()
            template = Template(html_text)
            return template.render(name=name )

    def get_concurs_info(self, name, con_link, status, date, town):
        with open(self.concurs_template_path, 'r', encoding='utf-8') as concr_temp:
            html_text = concr_temp.read()
            template = Template(html_text)
            return template.render(concurs_name=name, concurs__link=con_link, concurs_state=status, concurs_date=date,
                                   concurs_town=town)
