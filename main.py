from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.float.layout import FloatLayout
import time
import random
import requests

class MainApp(App):
  def build(self):
    
    layout = FloatLayout(size='auto') # Возможно, нужно сменить на цифры
    
    
    
    return layout
  
if __name__ == '__main__': 
  app = MainApp()
  app.run()
