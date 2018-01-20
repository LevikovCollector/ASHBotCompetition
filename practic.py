# import  re
# from datetime import datetime
# str1 = 'г. Новосибирск, УТВЕРЖДЕНО РК АСХ'
# str2 = 'г. Москва. Утверждено РК АСХ'
# str3 = 'г.Санкт-Петербург УТВЕРЖДЕНО РК АСХ'
# str4 = 'г. СПб, УТВЕРЖДЕНО РК АСХ'
# str5 = '(2016-11-13) Первенство Поволжья (Академия Танца)'
# str6 = '(2016-11-12) "Осенний кубок" (Априори) '
# str7 = 'г. Екатеринбург, УТВЕРЖДЕНО РК АСХ'
# str8 = 'г. Ростов-на-дону, УТВЕРЖДЕНО РК АСХ'
# str9 = '(2017-04-29,30) Чемпионат Урала по Хастлу 2017'
# str10 = '(2017-06-03/04) КОМАНДНОЕ ПЕРВЕНСТВО по хастлу.'
# str11 = '(2017-06-03/04) КОМАНДНОЕ ПЕРВЕНСТВО по хастлу.'
# str12 = '(2018-01-04 и 05) HOT WINTER CUP'
# str13 = '(2018-01-20) ICE CUP-2018'
# str14 = 'г.Санкт-Петербург, УТВЕРЖДЕНО РК АСХ'
#
#
# template1 = '[\s|\.|\,]'
# template2 = '\d\d\d\d-\d\d-\d\d+'
# template3 = '\s\D+'
# template4 = '[,/]\d+'
# template5 = '\d\d\d\d-\d\d-\d\d+|\s\D+'
from jinja2 import Template

with open('templates\greeting.html', 'r', encoding='utf-8') as temp:
    html_text = temp.read()
    template = Template(html_text)
    print(template.render())






