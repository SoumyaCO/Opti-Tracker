from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

KV = '''
ScreenManager:
    id: screen_manager
    LogoScreen:
        name: 'logoscreen'
        manager: screen_manager
    StartScreen:
        name: 'startscreen'
        manager: screen_manager
    CamScreen:
        name: 'Camscreen'
        manager: screen_manager

<LogoScreen>:
    canvas.before:
        Color:
            rgba:0,0,0,1 
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: "160dp"
        Image:
            source: 'logo.png'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.7, 0.7
        MDButton:
            style: "elevated"
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: root.manager.current = 'startscreen'
            MDButtonIcon:
                pos_hint: {'center_x': 0.6, 'center_y': 0.5}
                icon: "arrow-right"
            


        
<StartScreen>:
   
                
    canvas.before:
        # Color:
        #     rgba:
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        
        orientation: 'vertical'
        MDTopAppBar:
            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"
                    
            
            MDTopAppBarTitle:
                text: "OptiTracker"
                pos_hint: {"center_x": .5}
            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "account-circle-outline"
        BoxLayout:
            orientation: 'vertical'
           
            
            padding: "40dp"
            
            Image:
                source: 'optitrackers.png'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: 0.5, 0.5

           
            MDButton:
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                # padding: [0, 50, 0, 0] 
                on_release: 
                    root.manager.current = 'Camscreen'
                    root.manager.get_screen('Camscreen').start_camera()
                MDButtonText:
                    text: 'Get Started'

<CamScreen>:
    BoxLayout:
        orientation: 'vertical'
        Image:
            id: cam_image
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 2,2
        BoxLayout:
            size_hint_y: None
            height: "48dp"
            spacing: '120dp'
            padding: "30dp"
            pos_hint: {'center_x': 0.8, 'center_y': 0.5}
            MDButton:
                style: "elevated"
               
                on_release: root.start_camera()
                MDButtonText:
                    text: "Start"
            MDButton:
                style: "elevated"

                on_release: root.stop_camera()
                MDButtonText:
                    text: "Stop"
'''

class LogoScreen(MDScreen):
    pass

class StartScreen(MDScreen):
    pass

class CamScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CamScreen, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)

    def start_camera(self, *args):
        self.img1 = self.ids['cam_image']
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
        Clock.unschedule(self.update)
        self.capture.release()

class MainApp(MDApp):
    def build(self):     
        self.theme_cls.primary_palette = "Green"   
        return Builder.load_string(KV)

MainApp().run()
