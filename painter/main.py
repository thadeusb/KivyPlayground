import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.logger import Logger

CircleSize = 30.0
    
class MyPaintWidget(Widget):

        
    def on_motion(self, etype, motionevent, *args):    
        Logger.info(str(self))
        Logger.info(str(etype))
        Logger.info(str(motionevent))
        Logger.info(str(args))
        
    def on_touch_down(self, touch):
    
        Window.bind(on_motion=self.on_motion)
    
    
        touch.ud['color'] = (random.random(), 1, 1)    
        with self.canvas:
            Color(*touch.ud['color'], mode='hsv')
            Ellipse(pos=(touch.x - CircleSize/2, touch.y - CircleSize/2), 
                    size=(CircleSize,CircleSize))
                    
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]        
        
    
class MyPaintApp(App):

    def build(self):
        parent = Widget()
        painter = MyPaintWidget()
        clearbtn = Button(text='Clear Painting')
        
        parent.add_widget(painter)
        parent.add_widget(clearbtn)
        
        def clear_canvas(obj):
            painter.canvas.clear()
            
        clearbtn.bind(on_release=clear_canvas)
        
        return parent
        
if __name__ in ('__android__', '__main__'):
    MyPaintApp().run()
