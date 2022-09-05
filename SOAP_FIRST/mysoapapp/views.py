import pytz
from django.shortcuts import render
# Create your views here.
# views.py
user_timezone = pytz.timezone('Europe/Moscow')
import datetime as dt
from django.views.decorators.csrf import csrf_exempt
from spyne import AnyDict, Iterable
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import *
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from article.models import *
import re
from pytz import timezone
from django.utils.timezone import now



class SoapService(ServiceBase):
    #
    # Декоратор "@rpc(Unicode, _returns=Unicode)" определяет тип входящих аргументов («Unicode»)
    # и исходящих ответов ("_returns=Unicode").
    #
    # Аргумент «ctx»  информация о входящих запросах.

    #
    # Выдача  запись по ID и по title
    #
    @rpc(Unicode(nillable=True, default=None, min_occurs=1),
         Unicode(nillable=True, default=None), _returns=AnyDict)
    def get_article(ctx, id_, title_):
        if id_.isnumeric():
            id_ = int(id_)
            article = Article.objects.filter(id=id_)
        else:
            article = Article.objects.filter(title=title_)
        if article:
            context = {
                'id': article[0].id,
                'title': article[0].title,
                'content': article[0].content,
                'time_create': article[0].time_create,
                'time_update': article[0].time_update,
                'is_private': article[0].is_private,
                'author': article[0].author.email,
            }
        else:
            context = {
                'error': 'Запись не найдена',
            }
        return context

    #
    # Выдача всех записей ( с сорнтировкой_
    #
    @rpc( Unicode(nillable=True, default=None),_returns=Iterable(AnyDict))
    def get_all_article(ctx,orderby_):
        check_box = ['title','-title',
                     'time_create','-time_create',
                     'time_update','-time_update',
                     'is_private','-is_private',
                     'content','-content',
                     'author','-author']

        if orderby_ in check_box:
            article = Article.objects.all().order_by(orderby_)
        else:
            article = Article.objects.all()

        spisok = []
        if article:
            for i in article:
                context = {
                    'id': i.id,
                    'title': i.title,
                    'content': i.content,
                    'time_create': i.time_create,
                    'time_update': i.time_update,
                    'is_private': i.is_private,
                    'author': i.author.email,
                }
                spisok.append(context)
        else:
            context = {
                'error': 'Записей не найдено',
            }
            spisok.append(context)
        return spisok

    #
    # Добавление новой записи
    #
    @rpc(Unicode(nillable=False, min_occurs=1), Unicode(nillable=False, min_occurs=1),
         Unicode(nillable=False, min_occurs=1),
         Boolean(nillable=False, min_occurs=1), _returns=AnyDict)
    def addarticle(ctx, title, content, author, is_private):
        try:
            b2 = Article(title=title,
                         content=content,
                         time_create=dt.datetime.now(),
                         time_update=dt.datetime.now(),
                         # time_create=dt.datetime.now(),
                         # time_update=dt.datetime.now(),
                         is_private=is_private,
                         author=CustomUser.objects.get(email=author))
            b2.save()
            context = {
                'status': 'Успешно добавленная запись',
                'title': b2.title,
                'content': b2.content,
                'time_create': b2.time_create,
                'time_update': b2.time_update,
                'is_private': b2.is_private,
                'author': b2.author.email,
            }
        except:
            context = {
                'status': "Ошибка добавления записи",
            }
        return context

    #
    # Удаление запись по названию статьи
    #
    @rpc(Unicode(nillable=False, min_occurs=1), _returns=AnyDict)
    def delete_article(ctx, title):
        try:
            article = Article.objects.filter(title=title)
            context = {
                'status': 'Успешно удалена запись',
                'title': article[0].title,
                'content': article[0].content,
                'time_create': article[0].time_create,
                'time_update': article[0].time_update,
                'is_private': article[0].is_private,
                'author': article[0].author.email,
            }
            article.delete()
            # return context
        except:
            context = {
                'status': "Ошибка удаления записи",
            }
        return context

    #
    # Изменение запись
    #
    @rpc(Unicode(nillable=False, min_occurs=1), Unicode(nillable=True, default=None),
         Unicode(nillable=True, default=None),
         Unicode(nillable=True, default=None), _returns=AnyDict)
    def change_article(ctx, id_, title_, content_, is_private_):
        if id_.isnumeric():
            id_ = int(id_)
            article = Article.objects.filter(id=id_)
            if article:
                if title_ is None or len(title_) == 0:
                    title_ = article[0].title
                if content_ is None or len(content_) == 0:
                    content_ = article[0].content
                if is_private_ is None or len(is_private_) == 0 or (is_private_ != 'true' and is_private_ != 'false'):
                    is_private_ = article[0].is_private
                if is_private_ == 'false':
                    is_private_ = bool('')
                if is_private_ == 'true':
                    is_private_ = bool('1')

                article[0].title = title_
                article[0].content = content_
                # article[0].time_update = dt.datetime.now(tz)
                article[0].time_update = now().astimezone(user_timezone)
                article[0].is_private = is_private_
                article[0].save()
                context = {
                    'status': 'Успешно изменена запись',
                    'title': article[0].title,
                    'content': article[0].content,
                    'time_create': article[0].time_create,
                    'time_update': article[0].time_update,
                    'is_private': article[0].is_private,
                    'author': article[0].author.email,
                }
            else:
                context = {
                    "error": "Запись не найдена"
                }
        else:
            context = {
                "error": "Запись не найдена"
            }

        return context

    #
    # Регистрация пользователя
    #
    @rpc(Unicode(nillable=False, min_occurs=1), Unicode(nillable=False, min_occurs=1),
         Unicode(nillable=False, min_occurs=1), _returns=AnyDict)
    def register_user(self, email, username, password):
        pattern_email = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        pattern_password = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if (re.match(pattern_email, email) is not None) and (len(CustomUser.objects.filter(email=email)) == 0):
            if (re.match(pattern_password, password) is not None):
                user = CustomUser(username=username, email=email)
                user.set_password(password)
                user.save()
                сontext = {
                    'status': 'Пользователь успешно зарегистрирован',
                    'username': username,
                    'email': email
                }
            else:
                сontext = {
                    'error': "Неверный пароль"
                }
        else:
            сontext = {
                'error': "Неверный логин"
            }
        return сontext


# Переменная «soap_app» определяет настройки нашего веб-сервиса:


# «Application([SoapService]» — указывается, какой класс инициализируется (их может быть несколько),
# параметры «in_protocol» и «out_protocol» определяет тип входящих и исходящих запросов, в нашем случае это SOAP v1.1.
soap_app = Application(
    [SoapService],
    tns='mysoap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)
# django_soap_application = DjangoApplication(soap_app)
# csrf_exempt декоратор позволяет исключить представление из процесса проверки CSRF
my_soap_application = csrf_exempt(DjangoApplication(soap_app))
