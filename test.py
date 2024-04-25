import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class CamScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CamScreen, self).__init__(**kwargs)
        self.img1 = Image()
        self.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.img1.texture = image_texture

    def on_leave(self, *args):
        # close the camera properly
        self.capture.release()

class MainApp(MDApp):
    def build(self):     
        self.theme_cls.primary_palette = "Green"   
        return CamScreen()

MainApp().run()
