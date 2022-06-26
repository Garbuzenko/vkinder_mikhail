import random
from pprint import pprint

from psycopg2._psycopg import Boolean
import sqlalchemy

# from main import myApi
from modules.API.ClassVK import ClassVK
from modules.db.dataclasses import VKUserData

# класс для взаимодействия с базой данных
from modules.utils import utils


class DataBase(object):
    # функция инициализации класса
    def __init__(self, db_connection):
        self.db = db_connection
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    #Добавить в таблицу SEARCH пачку из 100 новых пользователей
    def update_search_list(self, user_id):
        myApi = ClassVK(utils.get_token('access_token'))
        count = 100
        offset = 10
        list = myApi.search( user_id, offset, count)
        pprint(list)
        return id

    #!!!Текущий обрабатываемый пользователь
    def get_next_user(self, user_id):
        self.move_offset(user_id, 1)
        myApi = ClassVK(utils.get_token('access_token'))
        id = myApi.search(user_id, offset=self.get_offset(user_id), count=1)[0]
        return id
    # !!!Предыдущий обрабатываемый пользователь
    def get_previous_user(self,user_id):
        self.move_offset(user_id, -1)
        myApi = ClassVK(utils.get_token('access_token'))
        id = myApi.search(user_id, offset=self.get_offset(user_id), count=1)[0]
        return id
    # !!!Текущий обрабатываемый пользователь
    def get_current_user(self,user_id):
        id = '100'
        return id
    #!!!получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites

    # !!!Сдвиг offset на число
    def move_offset(self, user_id, i):
        pass

    def get_offset(self, user_id):
        pass
        return random.randint(10, 100)
    #Настройки
    def get_setings(self, vk_user: VKUserData) -> Boolean:
        pass
        json_example = {'srch_offset': 1, 'age_from': 20, 'age_to': 30, 'access_token': ''}
        return json_example

    # функция получения данных пользователя ВКонтакте из базы данных
    def get_vkuser(self, vk_id : int) -> VKUserData:
        pass

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    def new_vkuser(self, vk_user : VKUserData) -> Boolean:
        pass

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id : int) -> Boolean:
        pass

    # сохранить в базе данных информацию об избранном контакте
    def new_favirite(self, vk_id : int, fav_id : int) -> Boolean:
        pass

    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id : int) -> Boolean:
        pass

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id : int) -> Boolean:
        pass

    # получить список заблокированных контактов
    def get_black_list(self, vk_id : int) -> list:
        pass
        black_list = [1000, 1001]
        return black_list

    # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id : int) -> Boolean:
        pass

    # удалить контакт из заблокированных
    def del_black_id(self, vk_id : int, blk_id : int) -> Boolean:
        pass

    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id : int) -> Boolean:
        pass



    #
    def update_settings(self, vk_user: VKUserData) -> Boolean:
        pass


# end class DataBase
