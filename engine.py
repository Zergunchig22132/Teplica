import requests
import time
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'True')


from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.properties import NumericProperty, StringProperty, ListProperty, DictProperty, ObjectProperty, BooleanProperty, BoundedNumericProperty, OptionProperty
from kivy.uix.pagelayout import PageLayout
from threading import Timer


# Я использую списки, длина которых больше на один элемент для удобства.
# Порядковый номер устройства является индексом его переменной в списке.
temperature = [0, 0, 0, 0, 0]
air_wetness = [0, 0, 0, 0, 0]
soil_wetness = [0, 0, 0, 0, 0, 0, 0]
vents_open = False
watering = [False, False, False, False, False, False, False]
air_humidification = False
manual_mode = False
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


def change_vents():
    if vents_open:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 0})
        vents_open = False
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 1})
        vents_open = True


def change_watering(num):
    if watering[num]:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=0))
		watering[num] = False
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=1))
		watering[num] = True


def change_air_humidification():
    if air_humidification:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=0))
        air_humidification = False
    else:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=1))
        air_humidification = True
		
def change_manual_mode():
	if manual_mode:
		manual_mode = False
	else:
		manual_mode = True

class MaketApp(App):
  def build(self):
    layout = BoxLayout(size = (1080, 1920))
    vents_button = Button(text = 'Переключить форточки', font_size = 14, on_press= change_vents())
    air_humidification_button = Button(text = 'Переключить увлажнители', font_size = 14, on_press = change_air_humidification())
	watering_button_1 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(1))
	watering_button_2 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(2))
	watering_button_3 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(3))
	watering_button_4 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(4))
	watering_button_5 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(5))
	watering_button_6 = Button(text = 'Полив 1', font_size = 14, on_press = change_watering(6))
	manual_mode_button = Button(text = 'Ручное управление', font_size = 14, on_press = change_manual_mode())
    
if __name__ == '__main__':
	MaketApp().run()
        
while True:
    get_air()
    get_soil_wetness()
    time.sleep(2)
