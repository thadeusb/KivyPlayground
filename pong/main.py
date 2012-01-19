import random

import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock

#: this has stuff defined in pong.kv to style it
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self, vel=(5,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, *args):
        self.ball.move()
        
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
            
        if (self.ball.x < 0):
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        
        if (self.ball.right > self.width):
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))
            
        if self.player1.score == 1:
            self.win_text.text = 'Player 1 Wins!'
            self.add_widget(self.win_text)
        elif self.player2.score == 1:
            self.win_text.text = 'Player 2 Wins!'
            self.add_widget(self.win_text)
            
            
            
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
            
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
    
class PongBall(Widget):
    
    #: velocity of ball
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    #: I figure that the underscore in the variables is some
    #: magic for making velocity.x and velocity.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        
class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            #: alias velocity
            vx, vy = ball.velocity
            #: cause ball to move y axis based on where
            #: on the paddle the ball hits
            offset = (ball.center_y-self.center_y)/(self.height/2)
            #: Calculate new vector
            bounced = Vector(-1*vx, vy)
            #: increase speed
            vel = bounced * 1.1
            #: set new velocity
            ball.velocity = vel.x, vel.y + offset
    
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
        
Factory.register("PongBall", PongBall)
Factory.register("PongPaddle", PongPaddle)
Factory.register("PongGame", PongGame)

if __name__ in ('__android__', '__main__'):
    PongApp().run()
