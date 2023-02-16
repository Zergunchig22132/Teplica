import requests
import time
import random
import multiprocessing as mp

from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivymd.uix.datatables import MDDataTable
from kivy.uix.spinner import Spinner

# Я использую списки, длина которых больше на один элемент для удобства.
# Порядковый номер устройства является индексом его переменной в списке.
temperature = [0, 0, 0, 0, 0]
mid_air_temp = 0
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
graph = True
temp_history = {}
mid_temp_history = {}
air_wetness_history = {}
mid_air_wet_history = {}
soil_wet_history = {}
mid_soil_wet_history = {}
start_time = time.time()
current_time = 0


def get_air(*args):
    global temperature, air_wetness, mid_air_temp, mid_air_wetness
    global start_time, current_time, temp_history, mid_temp_history
    global air_wetness_history, mid_air_wet_history
    current_time = time.time()
    localtemp, localwet = [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    time_dif = round(current_time - start_time, 2)
    for i in range(1, 5):
        json_temp = str(requests.get("https://dt.miet.ru/ppo_it/api/temp_hum/{}".format(str(i))).json())
        operational_list = json_temp.split()
        temperature[i] = float(str(operational_list[3])[0:-1])
        air_wetness[i] = float(str(operational_list[5])[0:-1])
        localtemp[i] = float(str(operational_list[3])[0:-1])
        localwet[i] = float(str(operational_list[5])[0:-1])
    print(air_wetness_history)
    print(temp_history)
    temp_history[time_dif] = localtemp
    air_wetness_history[time_dif] = localwet
    tempsum = 0
    for k in localtemp[1:]:
        tempsum += k
    mid_air_temp = round(tempsum / 4, 2)
    mid_temp_history[time_dif] = mid_air_temp
    tempsum = 0
    for j in localwet[1:]:
        tempsum += j
    mid_air_wetness = round(tempsum / 4, 2)
    mid_air_wet_history[time_dif] = mid_air_wetness


def get_soil_wetness(*args):
    global soil_wetness, mid_soil_wetness, start_time, current_time
    global soil_wet_history, mid_soil_wet_history, start_time
    current_time = time.time()
    localsoil = [0, 0, 0, 0, 0, 0, 0]
    time_dif = round(current_time - start_time, 2)
    for i in range(1, 7):
        json_soil = str(requests.get("https://dt.miet.ru/ppo_it/api/hum/{}".format(str(i))).json())
        json_soil = json_soil.split()
        soil_wetness[i] = float(str(json_soil[3])[0:-1])
        localsoil[i] = float(str(json_soil[3])[0:-1])
    soil_wet_history[time_dif] = localsoil
    mid_soil_wetness = round(sum(soil_wetness[1:]) / 6, 2)
    mid_soil_wet_history[time_dif] = mid_soil_wetness


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
    global mid_soil_wetness

    def update(self, *args):
        self.text = "СРЕДНЯЯ ВЛАЖНОСТЬ ПОЧВЫ: " + str(mid_soil_wetness) + " %"


class MidAirHumidificationLabel(Label):
    global mid_air_temp

    def update(self, *args):
        self.text = "ВЛАЖНОСТЬ ВОЗДУХА: " + str(mid_air_wetness) + " %"


class MidTemperatureLabel(Label):
    pos_hint_x = -0.1
    global mid_air_temp

    def update(self, *args):
        self.text = "СРЕДНЯЯ ТЕМПЕРАТУРА: " + str(mid_air_temp) + " °C"


class VentsButton(Button):
    global vents_open, mid_air_temp, max_air_temp, manual_mode

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif mid_air_temp > max_air_temp:
            self.disabled = False
        elif mid_air_temp <= max_air_temp and vents_open:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_vents()
        if vents_open:
            self.text = "Форточки открыты"
        else:
            self.text = "Форточки закрыты"


class AirWettingButton(Button):
    global air_wetness, mid_air_wetness, air_wetting, min_air_wetness
    global manual_mode

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif mid_air_wetness < min_air_wetness:
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
    global soil_wetness, min_soil_wetness, watering, manual_mode
    number = 1

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(1)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class WateringButton2(Button):
    global soil_wetness, min_soil_wetness, watering
    number = 2

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(2)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class WateringButton3(Button):
    global soil_wetness, min_soil_wetness, watering
    number = 3

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(3)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class WateringButton4(Button):
    global soil_wetness, min_soil_wetness, watering
    number = 4

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(4)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class WateringButton5(Button):
    global soil_wetness, min_soil_wetness, watering
    number = 5

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(5)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class WateringButton6(Button):
    global soil_wetness, min_soil_wetness, watering
    number = 6

    def update(self, *args):
        if manual_mode:
            self.disabled = False
        elif soil_wetness[self.number] < min_soil_wetness:
            self.disabled = False
        elif soil_wetness[self.number] > min_soil_wetness and watering[self.number]:
            self.disabled = False
        else:
            self.disabled = True

    def change_state(self, *args):
        change_watering(6)
        if watering[self.number]:
            self.text = "Полив грядки " + str(self.number) + "\nАктивен\n"
        else:
            self.text = "Полив грядки " + str(self.number) + "\nНеактивен\n"


class GraphLabel(Label):
    global temp_history, mid_temp_history
    global air_wetness_history, mid_air_wet_history
    global soil_wet_history, mid_soil_wet_history
    global start_time, current_time
    mode = "midtemp"  # Добавить такие режимы, как
    # "mid(temp, airwet, soilwet)"
    # "temp(1,2,3,4)"
    # "air(1,2,3,4)"
    # "soil(1,2,3,4,5,6)"
    time_period = [start_time, current_time]
    scale = 1
    trans = 0
    number = 4

    def set_graph_mode(self, mode, number):
        self.mode = mode
        self.number = number

    def update(self, *args):
        if graph:
            if self.mode == "midtemp":
                items = list(mid_temp_history.values())
                using = []
                for i in range(1, len(items) + 1):
                    using.append(items[-i])
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                else:
                    using = using[0:10]
                self.text = ''
                for j in using:
                    if len(str(j)) > 4:
                        self.text += str(j) + '°C' + '|' * int(j) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '°C' + "|" * int(j) + '\n'
            elif self.mode == "midairwet":
                items = list(mid_air_wet_history.values())
                using = []
                for i in range(1, len(items) + 1):
                    using.append(items[-i])
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                else:
                    using = using[0:10]
                self.text = ''
                for j in using:
                    if len(str(j)) > 4:
                        self.text += str(j) + '%' + '|' * int(j / 2) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '%' + "|" * int(j / 2) + '\n'
            elif self.mode == "midsoilwet":
                items = list(mid_soil_wet_history.values())
                using = []
                for i in range(1, len(items) + 1):
                    using.append(items[-i])
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                else:
                    using = using[0:10]
                self.text = ''
                for j in using:
                    if len(str(j)) > 4:
                        self.text += str(j) + '%' + '|' * int(j / 2) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '%' + "|" * int(j / 2) + '\n'
            elif self.mode == 'temp':
                items = list(temp_history.values())
                using = []
                for i in items:
                    using.append(i[self.number])
                using.reverse()
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                self.text = ''
                for j in using[0:10]:
                    if len(str(j)) > 4:
                        self.text += str(j) + '°C' + '|' * int(j) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '°C' + "|" * int(j) + '\n'
            elif self.mode == 'air':
                items = list(air_wetness_history.values())
                using = []
                for i in items:
                    using.append(i[self.number])
                using.reverse()
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                self.text = ''
                for j in using[0:10]:
                    if len(str(j)) > 4:
                        self.text += str(j) + '%' + '|' * int(j / 2) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '%' + "|" * int(j / 2) + '\n'
            elif self.mode == 'soil':
                items = list(soil_wet_history.values())
                using = []
                for i in items:
                    using.append(i[self.number])
                using.reverse()
                if len(using) < 10:
                    for k in range(10 - len(using)):
                        using.append(0)
                self.text = ''
                for j in using[0:10]:
                    if len(str(j)) > 4:
                        self.text += str(j) + '%' + '|' * int(j / 2) + '\n'
                    else:
                        self.text += str(j) + '0' * (5 - len(str(j))) + '%' + "|" * int(j / 2) + '\n'
        if not graph:
            if self.mode == "midtemp":
                keyslist = list(mid_temp_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_temp_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_temp_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == 'midsoilwet':
                keyslist = list(mid_soil_wet_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_soil_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_soil_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == "midairwet":
                keyslist = list(mid_air_wet_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_air_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_air_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == 'temp':
                keyslist = list(temp_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(temp_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    print(keyslist[-6:])
                    for k in keyslist[-6:]:
                        localvalue = str(temp_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == 'air':
                keyslist = list(air_wetness_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(air_wetness_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(air_wetness_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == 'soil':
                keyslist = list(soil_wet_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(soil_wet_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(soil_wet_history[k][self.number])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext



class Greenhouse_Automatic_Control_SystemApp(MDApp):
    global theme
    global mid_air_temp, max_air_temp

    def build(self):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = "Green"
        layout1 = BoxLayout(orientation='vertical')
        layout2 = BoxLayout(orientation='vertical')
        layout3 = BoxLayout(orientation='vertical')
        midtemplabel = MidTemperatureLabel()
        midairwetnesslabel = MidAirHumidificationLabel()
        midsoilwetnesslabel = MidSoilHumudificationLabel()
        vents_button = VentsButton(text='Форточки закрыты')
        vents_button.bind(on_press=vents_button.change_state)
        air_wetting_button = AirWettingButton(text="Увлажнители неактивны")
        air_wetting_button.bind(on_press=air_wetting_button.change_state)
        watering_button_1 = WateringButton1(text="Полив грядки 1 \n Неактивен")
        watering_button_1.bind(on_press=watering_button_1.change_state)
        watering_button_2 = WateringButton2(text="Полив грядки 2 \n Неактивен")
        watering_button_2.bind(on_press=watering_button_2.change_state)
        watering_button_3 = WateringButton3(text="Полив грядки 3 \n Неактивен")
        watering_button_3.bind(on_press=watering_button_3.change_state)
        watering_button_4 = WateringButton4(text="Полив грядки 4 \n Неактивен")
        watering_button_4.bind(on_press=watering_button_4.change_state)
        watering_button_5 = WateringButton5(text="Полив грядки 5 \n Неактивен")
        watering_button_5.bind(on_press=watering_button_5.change_state)
        watering_button_6 = WateringButton6(text="Полив грядки 6 \n Неактивен")
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

        layout1.add_widget(midtemplabel)
        layout1.add_widget(midairwetnesslabel)
        layout1.add_widget(midsoilwetnesslabel)
        layout1.add_widget(vents_button)
        layout1.add_widget(air_wetting_button)
        layout1.add_widget(watering_layout1)
        layout1.add_widget(watering_layout2)
        layout1.add_widget(watering_layout3)
        graph_label = GraphLabel()
        layout2.add_widget(graph_label)

        def graph_change(*args):
            global graph
            if graph:
                graph = not graph
                graph_button.text = "Используется\nтаблица"
            else:
                graph = not graph
                graph_button.text = "Используется\nграфик"

        def on_temp_enter(instance, value):
            global max_air_temp
            max_air_temp = int(value)

        max_temp_set = TextInput(multiline=False)
        max_temp_set.bind(text=on_temp_enter)
        temp_hint_label = Label(text='Максимальная\nтемпература:')
        setting1 = BoxLayout(orientation='horizontal')
        setting1.add_widget(temp_hint_label)
        setting1.add_widget(max_temp_set)

        def on_air_wet_enter(instance, value):
            global min_air_wetness
            min_air_wetness = int(value)

        min_air_wet_set = TextInput(multiline=False)
        min_air_wet_set.bind(text=on_air_wet_enter)
        air_wet_hint_label = Label(text='Минимальная\nвлажность\nвоздуха:')
        setting2 = BoxLayout(orientation='horizontal')
        setting2.add_widget(air_wet_hint_label)
        setting2.add_widget(min_air_wet_set)

        def on_soil_wet_enter(instance, value):
            global min_soil_wetness
            min_soil_wetness = int(value)

        soil_wet_hint_label = Label(text='Минимальная\nвлажность\nпочвы: ')
        min_soil_wet_set = TextInput(multiline=False)
        min_soil_wet_set.bind(text=on_soil_wet_enter)
        setting3 = BoxLayout(orientation='horizontal')
        setting3.add_widget(soil_wet_hint_label)
        setting3.add_widget(min_soil_wet_set)

        def manual_control_change(*args):
            global manual_mode
            manual_mode = not manual_mode

        manual_mode_switch = Switch(active=False)
        manual_mode_switch.bind(active=manual_control_change)
        manual_control_hint = Label(text='РУЧНОЕ\nУПРАВЛЕНИЕ')
        setting4 = BoxLayout(orientation='horizontal')
        setting4.add_widget(manual_control_hint)
        setting4.add_widget(manual_mode_switch)

        def token_change(instance, value):
            global token
            token = str(value)

        token_set = TextInput(multiline=False)
        token_set.bind(text=token_change)
        token_hint = Label(text="Токен:")
        setting5 = BoxLayout(orientation='horizontal')
        setting5.add_widget(token_hint)
        setting5.add_widget(token_set)
        graph_hint = Label(text='Переключение\nграфика:')
        graph_button = Button(text='Используется\nграфик')

        graph_button.bind(on_press=graph_change)
        setting6 = BoxLayout(orientation='horizontal')
        setting6.add_widget(graph_hint)
        setting6.add_widget(graph_button)
        layout3.add_widget(setting1)
        layout3.add_widget(setting2)
        layout3.add_widget(setting3)
        layout3.add_widget(setting4)
        layout3.add_widget(setting5)
        layout3.add_widget(setting6)

        current_mode_label = Label(text='Средняя температура')
        tempspinner = Spinner(text='Температура',
                              values=(
                                  'Средняя\nтемпература', 'Температура 1', 'Температура 2', 'Температура 3',
                                  'Температура 4')
                              )
        airwetspinner = Spinner(text='Влажность\nвоздуха',
                                values=(
                                    'Средняя\nвлажность\nвоздуха', 'Влажность\nвоздуха 1',
                                    'Влажность\nвоздуха 2', 'Влажность\nвоздуха 3',
                                    'Влажность\nвоздуха 4'
                                ))
        soilwetspinner = Spinner(text='Влажность\nпочвы',
                                 values=(
                                     'Средняя\nвлажность\nпочвы', 'Влажность\nпочвы 1',
                                     'Влажность\nпочвы 2', 'Влажность\nпочвы 3',
                                     'Влажность\nпочвы 4'
                                 ))

        def on_temp_spinner_set(spinner, text):
            if text == 'Средняя\nтемпература':
                graph_label.set_graph_mode('midtemp', 0)
                current_mode_label.text = 'Средняя температура'
            elif text == 'Температура 1':
                graph_label.set_graph_mode('temp', 1)
                current_mode_label.text = 'Датчик температуры 1'
            elif text == 'Температура 2':
                graph_label.set_graph_mode('temp', 2)
                current_mode_label.text = 'Датчик температуры 2'
            elif text == 'Температура 3':
                graph_label.set_graph_mode('temp', 3)
                current_mode_label.text = 'Датчик температуры 3'
            elif text == 'Температура 4':
                graph_label.set_graph_mode('temp', 4)
                current_mode_label.text = 'Датчик температуры 4'

        def on_air_wet_spinner_set(spinner, text):
            if text == 'Средняя\nвлажность\nвоздуха':
                graph_label.set_graph_mode('midairwet', 0)
                current_mode_label.text = 'Средняя влажность воздуха'
            elif text == 'Влажность\nвоздуха 1':
                graph_label.set_graph_mode('air', 1)
                current_mode_label.text = 'Датчик влажности 1'
            elif text == 'Влажность\nвоздуха 2':
                graph_label.set_graph_mode('air', 2)
                current_mode_label.text = 'Датчик влажности 2'
            elif text == 'Влажность\nвоздуха 3':
                graph_label.set_graph_mode('air', 3)
                current_mode_label.text = 'Датчик влажности 3'
            elif text == 'Влажность\nвоздуха 4':
                graph_label.set_graph_mode('air', 4)
                current_mode_label.text = 'Датчик влажности 4'

        def on_soil_wet_spinner_set(spinner, text):
            if text == 'Средняя\nвлажность\nпочвы':
                graph_label.set_graph_mode('midsoilwet', 0)
                current_mode_label.text = 'Средняя влажность почвы'
            elif text == 'Влажность\nпочвы 1':
                graph_label.set_graph_mode('soil', 1)
                current_mode_label.text = 'Датчик вляжности почвы 1'
            elif text == 'Влажность\nпочвы 2':
                graph_label.set_graph_mode('soil', 2)
                current_mode_label.text = 'Датчик вляжности почвы 2'
            elif text == 'Влажность\nпочвы 3':
                graph_label.set_graph_mode('soil', 3)
                current_mode_label.text = 'Датчик вляжности почвы 3'
            elif text == 'Влажность\nпочвы 4':
                graph_label.set_graph_mode('soil', 4)
                current_mode_label.text = 'Датчик вляжности почвы 4'
            elif text == 'Влажность\nпочвы 5':
                graph_label.set_graph_mode('soil', 5)
                current_mode_label.text = 'Датчик вляжности почвы 5'
            elif text == 'Влажность\nпочвы 6':
                graph_label.set_graph_mode('soil', 6)
                current_mode_label.text = 'Датчик вляжности почвы 6'

        spinner_layout = BoxLayout(orientation='horizontal')
        spinner_layout.add_widget(tempspinner)
        spinner_layout.add_widget(airwetspinner)
        spinner_layout.add_widget(soilwetspinner)

        tempspinner.bind(text=on_temp_spinner_set)
        airwetspinner.bind(text=on_air_wet_spinner_set)
        soilwetspinner.bind(text=on_soil_wet_spinner_set)

        current_mode_label.pos_hint = {'x':0, 'y':0.05}
        layout2.add_widget(spinner_layout)

        floatlayout2 = FloatLayout()
        floatlayout2.add_widget(layout2)
        floatlayout2.add_widget(current_mode_label)

        carousel = Carousel(direction="right", ignore_perpendicular_swipes=False, loop=True)
        carousel.add_widget(layout1)
        carousel.add_widget(floatlayout2)
        carousel.add_widget(layout3)

        def update_all(*args):
            global temperature, mid_temperature, air_wetness
            global mid_air_wetness, soil_wetness, mid_soil_wetness
            global vents_open, watering, air_wetting, manual_mode
            global max_air_temp, min_air_wetness, min_soil_wetness
            global temp_history, mid_temp_history, air_wetness_history
            global mid_air_wet_history, soil_wet_history, mid_soil_wet_history
            global start_time, current_time
            current_time = time.time()
            get_air()
            get_soil_wetness()
            current_time = time.time()
            midtemplabel.update()
            midairwetnesslabel.update()
            midsoilwetnesslabel.update()
            vents_button.update()
            air_wetting_button.update()
            watering_button_1.update()
            watering_button_2.update()
            watering_button_3.update()
            watering_button_4.update()
            watering_button_5.update()
            watering_button_6.update()
            graph_label.update()

        Clock.schedule_interval(update_all, 3)

        return carousel

    def on_start(self):
        global start_time
        start_time = time.time()


Greenhouse_Automatic_Control_SystemApp().run()
