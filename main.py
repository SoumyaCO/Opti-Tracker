from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image


KV = """
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
                size_hint: 1, 1
        
            MDDropDownItem:
                pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                padding: "-10dp"
                id: dropdown_item
                text: 'Select Camera'
                on_release: app.open_menu(self)
                MDDropDownItemText:
                    id: drop_text
                    text: "Select Cam"
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
            size_hint: 1,1
        BoxLayout:
            size_hint_y: None
            height: "58dp"
            spacing: '120dp'
            padding: "30dp"
            pos_hint: {'center_x': 0.9, 'center_y': 1}
           
            MDButton:
                style: "elevated"

                on_release: root.stop_camera()
                MDButtonText:
                    text: "Stop"
                
'''
selected_camera = 0 
class LogoScreen(MDScreen):
    pass


class StartScreen(MDScreen):
    pass


class CamScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CamScreen, self).__init__(**kwargs)
        global selected_camera
        self.capture = cv2.VideoCapture(selected_camera)

    def select_camera(self, value):
        global selected_camera  # Access the global variable
        selected_camera = int(value)  # Store the selected camera number
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(selected_camera)

    def start_camera(self, *args):
        if not self.capture:
            self.capture = cv2.VideoCapture(selected_camera)  # Use the selected camera number
        self.img1 = self.ids['cam_image']
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.img1.texture = image_texture
        # def start_camera(self, *args):
        # # Resume the camera 
        #     if self.capture:
        #         self.capture.play = True  # Start the camera

    def stop_camera(self, *args):
        # close the camera properly
        Clock.unschedule(self.update)
        if self.capture:
            self.capture.release()  # Stop the camera
            self.manager.current = "startscreen"


class MainApp(MDApp):
    def open_menu(self, item):
        menu_items = [
            {
                "text": i,
                "on_release": lambda x=i: self.menu_callback(item, x),
            }
            for i in ("0", "1")
        ]

        self.menu = MDDropdownMenu(
            caller=item,
            items=menu_items,
        )
        self.menu.open()

    def menu_callback(self, caller, text_item):
        
        caller.text = text_item
        # self.root.ids.drop_text.text = text_item
        self.root.get_screen('Camscreen').select_camera(text_item)
        self.menu.dismiss()

    def build(self):
        return Builder.load_string(KV)


MainApp().run()
