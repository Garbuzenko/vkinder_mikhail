###########################
# файл: databases.py
# version: 0.1.7
###########################
import sqlalchemy
from modules.db.dataclasses import VKUserData
# Глобальный переменные и классы модуля
POSTGRES_DB = 'postgresql://vkdbadmin:vk2022boT!!!@172.18.89.161:5432/vkusers'

# класс для взаимодействия с базой данных
class DataBase(object):

    # функция инициализации класса
    def __init__(self, db: str):
        self.db = db
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    # end __init__()

    # функция получения данных пользователя ВКонтакте из базы данных
    # возвращает объект типа VKUserData или None, если запрос неудачный (нет данных)
    def get_vkuser(self, vk_id: int) -> VKUserData:
        sql = f"""
            SELECT * FROM vk_users WHERE vk_id={vk_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если запрос выполнился успешно
        if result is not None:
            # заполняем и возвращаем объект VKUserData
            vk_user = VKUserData(list(result))
        else:
            # если запрос к базе данных ничего не вернул
            vk_user = None
        return vk_user

    # get_vkuser()

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    # возвращае True, если данные сохранены в базе данных, иначе False
    def new_vkuser(self, vk_user: VKUserData) -> bool:
        sql = f"""
            SELECT * FROM vk_users WHERE vk_id={vk_user.vk_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если запрос выполнился успешно
        if result is None:
            # нет такого пользователя в базе данных
            sql = f"""
                INSERT INTO vk_users (vk_id,first_name,last_name,bdate,gender,city_id,city_title,vkdomain,last_visit) 
                VALUES ({vk_user.vk_id},'{vk_user.first_name}','{vk_user.last_name}','{vk_user.bdate}',{vk_user.gender},{vk_user.city_id},'{vk_user.city_title}','{vk_user.vkdomain}','{vk_user.last_visit}');
                """
        else:
            # пользователь уже существует в базе данных
            sql = f"""
                UPDATE vk_users SET last_visit = '{vk_user.last_visit}' WHERE vk_id = {vk_user.vk_id};
                """
        result = self.connection.execute(sql)
        # если запрос выполнился с ошибкой
        if result is None:
            return False
        # успешный результат
        return True

    # enf new_vk_user

    #Вставить массив данных в last_search
    def insert_last_search(self, user_id, lst_ids, position):
        for lst_id in lst_ids:
            sql = f"""SELECT * FROM last_search WHERE vk_id='{user_id}' and lst_id='{lst_id}';
            """
            result = self.connection.execute(sql).fetchone()
            if result is None:
                sql = f"""INSERT INTO last_search(vk_id, lst_id, srch_number) VALUES ('{user_id}','{lst_id}','{position}');
                              """
                print(sql)
                result = self.connection.execute(sql)
                position += 1

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id: int) -> bool:
        pass


    # сохранить в базе данных информацию об избранном контакте
    def new_favorite(self, vk_id: int, fav_id: int) -> bool:
        pass

    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id: int) -> bool:
        pass

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id: int) -> bool:
        pass

    # получить список заблокированных контактов
    def get_black_list(self, vk_id: int) -> list:
        pass

    # # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id: int) -> bool:
        pass

    # удалить контакт из заблокированных
    def del_black_id(self, vk_id: int, blk_id: int) -> bool:
        pass

    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id: int) -> bool:
        pass

    # считать дополнительные данные о пользователе из базы данных
    def get_setings(self, vk_user: VKUserData) -> bool:
        sql = f"""
            SELECT * FROM settings WHERE vk_id={vk_user.vk_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если запрос выполнился успешно
        if result is not None:
            # заполняем и возвращаем объект VKUserData
            # нулевой элемент списка это vk_id из таблицы bd.search
            vk_user.set_settings_from_list(list(result)[1:])
        else:
            # если запрос к базе данных ничего не вернул
            vk_user.set_default_settings()
            return False
        return vk_user

    def get_user(self, user_id, rch_number):
        sql = f"""
               SELECT lst_id FROM last_search WHERE vk_id={user_id} AND srch_number = {rch_number} LIMIT 1;
               """
        result = self.connection.execute(sql).fetchone()
        return result

    #!!!получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites

    def set_setings(self, user_id, access_token='', srch_offset=0, age_from=20, age_to=50, last_command=''):
        sql = f"""
        INSERT INTO settings(vk_id, access_token, srch_offset, age_from, age_to, last_command) 
        VALUES ('{user_id}','{access_token}','{srch_offset}','{age_from}','{age_to}','{last_command}');
               """
        self.connection.execute(sql)

    def upd_setings(self, user_id, access_token='', srch_offset=0, age_from=20, age_to=50, last_command=''):


        sql = f"""
        UPDATE settings SET srch_offset = '{srch_offset}' where vk_id={user_id};
               """
        res = self.connection.execute(sql)

    # #Настройки
    # def get_setings_2(self, user_id):
    #     sql = f"""
    #               SELECT * FROM settings WHERE vk_id={user_id} LIMIT 1;
    #               """
    #     result = self.connection.execute(sql).fetchone()
    #     return result

