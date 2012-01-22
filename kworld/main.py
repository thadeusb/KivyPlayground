import kivy

kivy.require('1.0.9')

import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

FPS = 1.0/60.0

class Agent():
    def __init__(self):
        self.pos = Vector(0,0)
        self.target = Vector(0,0)

class KaboodleGame(Widget):
    def __init__(self, *args, **kwargs):
        super(KaboodleGame, self).__init__(*args, **kwargs)

        self.initialized = False

        Clock.schedule_once(self.initialize)

    def initialize(self, dt):
        self.initialized = True

        try:
            self.window_width
            self.window_height
        except AttributeError:
            win = self.get_parent_window()

            self.window_width = win.width
            self.window_height = win.height

        self.agents = []

        for i in range(30):
            a = Agent()
            a.pos = Vector(random.uniform(0, self.window_width),
                           random.uniform(0, self.window_height))
            a.target = Vector(random.uniform(0, self.window_width),
                              random.uniform(0, self.window_height))

            self.agents.append(a)

        self.selected = self.agents[random.randrange(0, len(self.agents))]

        Clock.schedule_interval(self.update, FPS)
        Clock.schedule_interval(self.alter_targets, 5)

    def alter_targets(self, dt):
        for a in self.agents:
            if a == self.selected:
                continue

            a.target = Vector(random.uniform(0, self.window_width),
                              random.uniform(0, self.window_height))

    def on_touch_down(self, touch):
        for a in self.agents:
            if a.pos.distance(Vector(touch.x, touch.y)) < 20:
                self.selected = a

    def on_touch_up(self, touch):
        self.selected.target = Vector(touch.x, touch.y)

    def update(self, dt):
        for agent in self.agents:
            dir = agent.target - agent.pos

            if dir.length() > 8:
                agent.pos += dir.normalize() * 7

        for a in self.agents:
            for a2 in self.agents:
                if a2 == a:
                    continue

                d = a.pos.distance(a2.pos)

                if 2 < d < 44:
                    # resolve collision
                    overlap = 44 - d

                    if self.selected in (a, a2):
                        if a2 == self.selected:
                            other = a
                        else:
                            other = a2

                        direction = other.pos - self.selected.pos
                        direction = direction.normalize() * overlap / 2

                        other.pos += direction
                    else:
                        direction = a2.pos - a.pos
                        direction = direction.normalize() * overlap / 2

                        a2.pos += direction
                        a.pos -= direction

        self.draw()

    def draw(self):
        self.canvas.clear()

        with self.canvas:
            Color(1,1,1)
            Rectangle(pos=(0,0), size=self.size)

            for agent in self.agents:
                Color(1,0,0)
                Ellipse(pos=(agent.target[0]-15,
                             agent.target[1]-15), size=(30*2, 30*2))
                Color(1,1,1)
                Ellipse(pos=(agent.target[0]-15+1,
                             agent.target[1]-15+1), size=(29*2, 29*2))

            for agent in self.agents:
                Color(0,0,0)
                Ellipse(pos=(agent.pos[0]-10-1,
                             agent.pos[1]-10-1), size=(21*2,21*2))

                if agent == self.selected:
                    Color(200/255.0,250/255.0,1)
                else:
                    Color(200/255.0,200/255.0,1)

                Ellipse(pos=(agent.pos[0]-10,
                             agent.pos[1]-10), size=(20*2, 20*2))

class KaboodleWorldApp(App):
    def build(self):
        game = KaboodleGame()
        return game

if __name__ in ('__android__', '__main__'):
    KaboodleWorldApp().run()
