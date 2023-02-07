from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import random


class Mainball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class ballGame(Widget):
    ball = ObjectProperty(None)
    
    def create_ball(self):
        self.ball.center = self.center
        self.ball.velocity =
    
class ballApp(App):
    def build(self):
        return Mainball()


if __name__ == '__main__':
    ballApp().run()
