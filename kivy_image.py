from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class CamApp(App):
    def build(self):
        self.img = Image()
        layout = BoxLayout()
        layout.add_widget(self.img)

        self.capture = cv2.VideoCapture(
            1
        )  # for me it's "1", adjust your webcams/cameras
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 frames per second
        return layout

    def update(self, dt):
        cap = self.capture
        _, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        buffer = cv2.flip(image, 0).tobytes()
        texture_new = Texture.create(
            size=(image.shape[1], image.shape[0]), colorfmt="luminance"
        )
        texture_new.blit_buffer(buffer, colorfmt="luminance", bufferfmt="ubyte")
        self.img.texture = texture_new


if __name__ == "__main__":
    CamApp().run()
    cv2.destroyAllWindows()

