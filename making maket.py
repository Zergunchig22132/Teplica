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


class MaketApp(App):
  def build(self):
    layout = BoxLayout(size = (1080, 1920))
    vents_button = Button(text = 'Переключить форточки', font_size = 14, on_press(change_vents))
    air_fumigation_button = Button(text = 'Переключить увлажнители', font_size = 14, on_press(change_air_fumigation))
