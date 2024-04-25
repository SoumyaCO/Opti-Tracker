from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu

from kivymd.app import MDApp

KV = '''
MDScreen
    md_bg_color: self.theme_cls.backgroundColor

    MDDropDownItem:
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.open_menu(self)

        MDDropDownItemText:
            id: drop_text
            text: "Item"
'''


class Example(MDApp):
    def open_menu(self, item):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item):
        self.root.ids.drop_text.text = text_item

    def build(self):
        return Builder.load_string(KV)


Example().run()