import json
import random
from pprint import pprint

import tqdm as tqdm
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import json
import random

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# from main import myApi
from modules.API.ClassVK import ClassVK
from modules.data.data import settings
from modules.data.data import comands

def get_token(name):
    with open('D:/token/tokens.json') as f:
        token_json = json.load(f)
    return token_json[name]

def get_answer(el):
    answer = f'{random.choice(el["out"])} {el.get("content")}'
    return answer

def get_comand(request):
    c = 'none'
    for c in comands:
        el = comands[c]
        if request in el.get('in') or request == c:
            break
    comand = comands[c]
    return comand
