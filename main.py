from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



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
        
        Image:
            source: 'logo.png'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.3, 0.3
        MDButton:
            style: "elevated"
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: root.manager.current = 'startscreen'
            MDButtonIcon:
                icon: "arrow-right"
            MDButtonText:
                text: "Launch"


        
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
            Image:
                source: 'optitrackers.png'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: 0.5, 0.5
        MDButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            # padding: [0, 50, 0, 0] 
            on_release: root.manager.current = 'CamScreen'
            MDButtonText:
                text: 'Get Started'

<CamScreen>:
    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'optitrackers.png'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.5, 0.5


'''

class LogoScreen(MDScreen):
    pass

class StartScreen(MDScreen):
    pass

class CamScreen(MDScreen):
    pass


class MainApp(MDApp):
    def build(self):     
        self.theme_cls.primary_palette = "Green"   
        return Builder.load_string(KV)

MainApp().run()

