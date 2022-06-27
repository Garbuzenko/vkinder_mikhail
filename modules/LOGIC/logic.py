from pprint import pprint

from vk_api.bot_longpoll import VkBotEventType
import json




class Logic(object):

    # функция инициализации класса
    def __init__(self, db, api):
        self.db = db
        self.api = api
        self.position = 0

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
        # return self.settings
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
