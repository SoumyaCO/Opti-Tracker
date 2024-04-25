from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:

            
        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0

            MDNavigationDrawerMenu:

                MDNavigationDrawerLabel:
                    text: "Mail"

                MDNavigationDrawerItem:

                    MDNavigationDrawerItemLeadingIcon:
                        icon: "account"

                    MDNavigationDrawerItemText:
                        text: "Inbox"

                    MDNavigationDrawerItemTrailingText:
                        text: "24"

                MDNavigationDrawerDivider:
'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)


Example().run()