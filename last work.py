import requests
import time
import random

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.icon_definitions import md_icons
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.button import Button

# Я использую списки, длина которых больше на один элемент для удобства.
# Порядковый номер устройства является индексом его переменной в списке.
temperature = [0, 0, 0, 0, 0]
mid_temperature = 0
air_wetness = [0, 0, 0, 0, 0]
mid_air_wetness = 0
soil_wetness = [0, 0, 0, 0, 0, 0, 0]
mid_soil_wetness = 0
vents_open = False
watering = [False, False, False, False, False, False, False]
air_humidification = False
manual_mode = False
token = ""
font = 14
theme = "Dark"
highest_air_temp = 29


def get_air():
    global temperature, air_wetness, mid_temperature, mid_air_wetness
    for i in range(1, 5):
        json_temp = str(requests.get("https://dt.miet.ru/ppo_it/api/temp_hum/{}".format(str(i))).json())
        operational_list = json_temp.split()
        temperature[i] = float(str(operational_list[3])[0:-1])
        air_wetness[i] = float(str(operational_list[5])[0:-1])
    tempsum = 0
    for k in temperature[1:]:
        tempsum += k
    mid_temperature = round(tempsum / 4, 2)

def get_soil_wetness():
    global soil_wetness, mid_soil_wetness
    for i in range(1, 7):
        json_soil = str(requests.get("https://dt.miet.ru/ppo_it/api/hum/{}".format(str(i))).json())
        json_soil = json_soil.split()
        soil_wetness[i] = float(str(json_soil[3])[0:-1])
    mid_soil_wetness = round(sum(soil_wetness[1:]) / 6, 2)


def change_vents():
    global vents_open
    if vents_open:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 0})
        vents_open = False
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', data={'state': 1})
        vents_open = True


class MidSoilHumudificationLabel(Label):
    global soil_wetness, mid_soil_wetness

    def update(self, *args):
        get_soil_wetness()
        self.text = "СРЕДНЯЯ ВЛАЖНОСТЬ ПОЧВЫ: " + str(mid_soil_wetness) + " %"


class MidAirHumidificationLabel(Label):
    global mid_air_wetness, air_wetness

    def update(self, *args):
        get_air()
        self.text = "ВЛАЖНОСТЬ ВОЗДУХА: " + str(mid_temperature) + " %"


class MidTemperatureLabel(Label):
    pos_hint_x = -0.1
    global temperature, mid_temperature

    def update(self, *args):
        get_air()
        self.text = "СРЕДНЯЯ ТЕМПЕРАТУРА: " + str(mid_temperature) + " °C"


class VentsButton(Button):
    disabled = False
    global vents_open, mid_temperature, highest_air_temp
    text = 'Форточки закрыты'

    def update(self, *args):
        get_air()
        if mid_temperature > highest_air_temp:
            self.disabled = False
        elif mid_temperature <= highest_air_temp and vents_open == True:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_vents()
        if vents_open:
            self.text = "Форточки открыты"
        else:
            self.text = "Форточки закрыты"


class TestApp(MDApp):
    global theme
    global mid_temperature

    def build(self):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = "Green"
        layout = BoxLayout(orientation='vertical')
        midtemplabel = MidTemperatureLabel()
        midairwetnesslabel = MidAirHumidificationLabel()
        midsoilwetnesslabel = MidSoilHumudificationLabel()
        ventsbutton = VentsButton()
        ventsbutton.bind(on_press=ventsbutton.change_state)
        layout.add_widget(midtemplabel)
        layout.add_widget(midairwetnesslabel)
        layout.add_widget(midsoilwetnesslabel)
        layout.add_widget(ventsbutton)
        page1 = MDBottomNavigationItem(
            layout,
            text='УПРАВЛЕНИЕ',
        )
        bottomnav = MDBottomNavigation(page1)
        Clock.schedule_interval(midtemplabel.update, 0.25)
        Clock.schedule_interval(midairwetnesslabel.update, 0.25)
        Clock.schedule_interval(midsoilwetnesslabel.update, 0.25)
        Clock.schedule_interval(ventsbutton.update, 0.25)
        return bottomnav


TestApp().run()
