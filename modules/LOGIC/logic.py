from pprint import pprint

from vk_api.bot_longpoll import VkBotEventType
import json




class Logic(object):

    # функция инициализации класса
    def __init__(self, db, api):
        self.db = db
        self.api = api
        self.position = 0

    def update_search_list(self, user_id):
        count = 10
        offset = 10
        position = self.position
        list = self.api.search(user_id, offset, count)
        for l in list:
            sql = f"""SELECT * FROM last_search WHERE vk_id='{user_id}' and lst_id='{l}';
                   """
            print(sql)
            result = self.connection.execute(sql).fetchone()
            if result is None:
                sql = f"""INSERT INTO last_search(vk_id, lst_id, srch_number) VALUES ('{user_id}','{l}','{position}');
                       """
                print(sql)
                result = self.connection.execute(sql).fetchone()
                position += 1
        return id

    def get_user(self, user_id, position):
        user = self.db.get_user(user_id, self.position)
        if user is None:
            self.update_search_list(user_id)
            user = self.db.get_user(user_id, self.position)
        return user


    #Следующий обрабатываемый пользователь
    def get_next_user(self, user_id):
        self.position += 1
        return self.api.get_user_data(self.db.get_user(user_id, self.position))

    #Предыдущий обрабатываемый пользователь
    def get_previous_user(self, user_id):
        self.position += -1
        return self.api.get_user_data(self.db.get_user(user_id, self.position))

    #Текущий обрабатываемый пользователь
    def get_current_user(self, user_id):
        return self.api.get_user_data( self.db.get_user(user_id, self.position))

    #получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites

    def get_settings(self, user_id: int):
        settings = self.db.get_setings(user_id)
        if settings is None:
            self.db.set_setings(user_id=user_id)
            settings = self.db.get_setings(user_id)
        pprint(settings)
        self.position = settings[2]

    def set_settings(self, user_id: int):
        self.db.set_setings(user_id=user_id,srch_offset=self.position)

    def upd_settings(self, user_id: int):
        self.db.upd_setings(user_id=user_id, srch_offset=self.position)

    def get_user_id(self, event):
        if  event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            user_id = event.object.user_id
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            user_id = None
        else:
            user_id = None
            print(f'ERROR EVENT {event}')
        return user_id
