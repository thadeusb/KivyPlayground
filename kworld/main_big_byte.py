import kivy

kivy.require('1.0.9')

import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

FPS = 1.0/60.0

class Noodle(Widget):
    SPEED = 4
    ENERGY_CONSUMPTION = .1

    size = (5,5)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, velocity=(0,0), **kwargs):
        super(Noodle, self).__init__(**kwargs)

        self.velocity = velocity
        self.speed = Noodle.SPEED

        self.hunger = 100

        self.color = (1, random.random(), random.random())

        self.velocity_x += random.random() - random.random()
        self.velocity_y += random.random() - random.random()

    def update(self, *args):
        self.move()

        food = self.parent.i_collide_food(self)

        if food:
            self.eat(food)

        self.render()

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

        if (self.x < 0) or (self.right > self.parent.window_width):
            self.velocity_x *= -1
        if (self.y < 0) or (self.top > self.parent.window_height):
            self.velocity_y *= -1

        self.hunger -= Noodle.ENERGY_CONSUMPTION

        if self.hunger <= 0:
            self.die()

    def render(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)

    def die(self):
        Clock.unschedule(self.update)

        if not self.parent:
            return

        def end(dt):
            if self.parent:
                self.parent.remove_widget(self)

        Clock.schedule_once(end, 0.25)

    def eat(self, food):
        self.hunger += food.energy_potential

        self.parent.remove_widget(food)
        self.parent.food.remove(food)

class Food(Widget):
    ENERGY_POTENTIAL = 15

    size = (5,5)

    def __init__(self, energy_potential=ENERGY_POTENTIAL, **kwargs):
        super(Food, self).__init__(**kwargs)

        self.energy_potential = energy_potential

    def update(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0)
            Ellipse(pos=self.pos, size=self.size)

class KaboodleGame(Widget):

    def __init__(self, *args, **kwargs):
        super(KaboodleGame, self).__init__(*args, **kwargs)

        self.initialized = False
        self.food = []
        self.noodles = []

        Clock.schedule_once(self.initialize)
        Clock.schedule_interval(self.update, FPS)
        Clock.schedule_interval(self.spawn_food, 5)

    def initialize(self, dt):
        self.initialized = True

        try:
            self.window_width
            self.window_height
        except AttributeError:
            win = self.get_parent_window()

            self.window_width = win.width
            self.window_height = win.height

        self.add_noodles()
        self.spawn_food()

    def add_noodles(self):
        for i in range(50):
            person = Noodle(pos=(random.randrange(self.window_width),
                                 random.randrange(self.window_height)))
            self.noodles.append(person)
            self.add_widget(person)

    def spawn_food(self, dt=0.0):

        for i in range(5):
            x_center = random.randrange(self.window_width)
            y_center = random.randrange(self.window_height)

            for i in range(15):
                x = random.randrange(x_center-15, x_center+15)
                y = random.randrange(y_center-15, y_center+15)

                if 0 < x < self.window_width \
                and 0 < y < self.window_height:
                    food = Food(pos=(x, y))
                    self.food.append(food)
                    self.add_widget(food)



    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.2, .5, .2)
            Rectangle(pos=(0,0), size=self.size)

        for noodle in self.noodles:
            noodle.update()

class KaboodleWorldApp(App):
    def build(self):
        game = KaboodleGame()
        return game

if __name__ in ('__android__', '__main__'):
    KaboodleWorldApp().run()
