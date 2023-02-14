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


class MidAirHumidificationLabel(Label):
    global mid_air_wetness, 

    def update(self *args):
        get_air()
        self.text = "ВЛАЖНОСТЬ ВОЗДУХА: "


class MidTemperatureLabel(Label):
    global temperature
    global mid_temperature

    def update(self, *args):
        get_air()
        self.text = "СРЕДНЯЯ ТЕМПЕРАТУРА: " + str(mid_temperature) + " °C"


class TestApp(MDApp):
    global theme
    global mid_temperature

    def build(self):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = "Green"
        layout = BoxLayout()
        midtemplabel = MidTemperatureLabel()
        page1 = MDBottomNavigationItem(
            midtemplabel,
            text='УПРАВЛЕНИЕ',
        )
        bottomnav = MDBottomNavigation(page1)
        layout.add_widget(bottomnav)
        Clock.schedule_interval(midtemplabel.update, 0.5)
        return layout


TestApp().run()
