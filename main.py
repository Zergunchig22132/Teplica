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
air_wetting = False
manual_mode = False
token = ""
font = 14
theme = "Dark"
max_air_temp = 29
min_air_wetness = 30
min_soil_wetness = 72


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

def change_watering(num):
    global watering
    if watering[num]:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=0))
        watering[num] = False
    else:
        requests.patch('https://dt.miet.ru/ppo_it/api/watering', data=dict(id=num, state=1))
        watering[num] = True


def change_air_humidification():
    global air_wetting
    if air_wetting:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=0))
        air_wetting = False
    else:
        requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", data=dict(state=1))
        air_wetting = True


def change_manual_mode():
    global manual_mode
    if manual_mode:
        manual_mode = False
    else:
        manual_mode = True


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
    global vents_open, mid_temperature, max_air_temp

    def update(self, *args):
        get_air()
        if mid_temperature > max_air_temp:
            self.disabled = False
        elif mid_temperature <= max_air_temp and vents_open:
            self.disabled = False
        else:
            self.disabled = True
        if vents_open:
            self.text = "Форточки открыты"
        else:
            self.text = "Форточки закрыты"

    def change_state(self, *args):
        change_vents()
        if vents_open:
            self.text = "Форточки открыты"
        else:
            self.text = "Форточки закрыты"


class AirWettingButton(Button):
    global air_wetness, mid_air_wetness, air_wetting, min_air_wetness

    def update(self, *args):
        get_air()
        if mid_air_wetness < min_air_wetness:
            self.disabled = False
        elif mid_air_wetness > min_air_wetness and air_wetting:
            self.disabled = False
        else:
            self.disabled = True
        if air_wetting:
            self.text = "Увлажнители активны"
        else:
            self.text = "Увлажнители неактивны"

    def change_state(self, *args):
        change_air_humidification()
        if air_wetting:
            self.text = "Увлажнители активны"
        else:
            self.text = "Увлажнители неактивны"


class WateringButton1(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 1

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


class WateringButton2(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 2

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


class WateringButton3(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 3

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


class WateringButton4(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 4

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


class WateringButton5(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 5

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


class WateringButton6(Button):
    global soil_wetness, mid_soil_wetness, watering
    number = 6

    def update(self, *args):
        get_soil_wetness()
        if soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n" + "Влажность: " + str(soil_wetness[self.number]) + "%"


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
        vents_button = VentsButton()
        vents_button.bind(on_press=vents_button.change_state)
        air_wetting_button = AirWettingButton()
        air_wetting_button.bind(on_press=air_wetting_button.change_state)
        watering_button_1 = WateringButton1()
        watering_button_1.bind(on_press=watering_button_1.change_state)
        watering_button_2 = WateringButton2()
        watering_button_2.bind(on_press=watering_button_2.change_state)
        watering_button_3 = WateringButton3()
        watering_button_3.bind(on_press=watering_button_3.change_state)
        watering_button_4 = WateringButton4()
        watering_button_4.bind(on_press=watering_button_4.change_state)
        watering_button_5 = WateringButton5()
        watering_button_5.bind(on_press=watering_button_5.change_state)
        watering_button_6 = WateringButton6()
        watering_button_6.bind(on_press=watering_button_6.change_state)
        watering_layout1 = BoxLayout(orientation='horizontal')
        watering_layout2 = BoxLayout(orientation='horizontal')
        watering_layout3 = BoxLayout(orientation='horizontal')
        watering_layout1.add_widget(watering_button_1)
        watering_layout1.add_widget(watering_button_2)
        watering_layout2.add_widget(watering_button_3)
        watering_layout2.add_widget(watering_button_4)
        watering_layout3.add_widget(watering_button_5)
        watering_layout3.add_widget(watering_button_6)
        layout.add_widget(midtemplabel)
        layout.add_widget(midairwetnesslabel)
        layout.add_widget(midsoilwetnesslabel)
        layout.add_widget(vents_button)
        layout.add_widget(air_wetting_button)
        layout.add_widget(watering_layout1)
        layout.add_widget(watering_layout2)
        layout.add_widget(watering_layout3)
        page1 = MDBottomNavigationItem(
            layout,
            text='УПРАВЛЕНИЕ',
        )
        bottomnav = MDBottomNavigation(page1)
        Clock.schedule_interval(midtemplabel.update, 0.5)
        Clock.schedule_interval(midairwetnesslabel.update, 0.5)
        Clock.schedule_interval(midsoilwetnesslabel.update, 0.5)
        Clock.schedule_interval(vents_button.update, 0.5)
        Clock.schedule_interval(air_wetting_button.update, 0.5)
        Clock.schedule_interval(watering_button_1.update, 0.5)
        Clock.schedule_interval(watering_button_2.update, 0.5)
        Clock.schedule_interval(watering_button_3.update, 0.5)
        Clock.schedule_interval(watering_button_4.update, 0.5)
        Clock.schedule_interval(watering_button_5.update, 0.5)
        Clock.schedule_interval(watering_button_6.update, 0.5)
        return bottomnav


TestApp().run()
