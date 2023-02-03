import requests
import time

# Я использую списки, длина которых больше на один элемент для удобства.
# Порядковый номер устройства является индексом его переменной в списке.
temperature = [0, 0, 0, 0, 0]
air_wetness = [0, 0, 0, 0, 0]
soil_wetness = [0, 0, 0, 0, 0, 0, 0]
vents_open = False
watering = [False, False, False, False, False, False, False]
air_humidification = False
operational_list = []
token = ""


def get_air():
    for i in range(1, 5):
        json_temp = str(requests.get("https://dt.miet.ru/ppo_it/api/temp_hum/{}".format(str(i))).json())
        operational_list = json_temp.split()
        temperature[i] = float(str(operational_list[3])[0:-1])
        air_wetness[i] = float(str(operational_list[5])[0:-1])


def get_soil_wetness():
    for i in range(1, 7):
        json_soil = str(requests.get("https://dt.miet.ru/ppo_it/api/hum/{}".format(str(i))).json())
        json_soil = json_soil.split()
        soil_wetness[i] = float(str(json_soil[3])[0:-1])


def set_vents(state):
    if state:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 1})
        vents_open = True
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 0})
        vents_open = False


def set_watering(num, state):
    if state:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=1))
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=2))


def set_fumigation(state):
    if state:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=1))
        air_humidification = True
    else:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=0))
        air_humidification = False


while True:
    get_air()
    get_soil_wetness()
    time.sleep(2)
