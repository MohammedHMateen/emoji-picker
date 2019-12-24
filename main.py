from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.svg import Svg
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scatter import Scatter

from emoji_dictionary import EmojiDictionary

class EmojiKeyboard(BoxLayout):

    search_filter = ''
    orientation = 'vertical'
    spacing = 20

    def __init__(self, **kwargs):
        super(EmojiKeyboard, self).__init__(**kwargs)

        self.emoji_dictionary = EmojiDictionary()

        self.emoji_grid = EmojiGrid()
        self.filterInput = TextInput(multiline=False, size_hint_y=None, height=50)
        self.filterInput.focus = True
        self.filterInput.bind(text=self.on_filter_text)

        self.add_widget(self.filterInput)
        self.add_widget(self.emoji_grid)


    def on_filter_text(self, instance, value):
        self.emoji_grid.items = self.emoji_dictionary.search(value, max_items=50)


class EmojiGrid(StackLayout):

    items = ListProperty([])
    spacing = (20, 20)

    def __init__(self, **kwargs):
        super(EmojiGrid, self).__init__(**kwargs)

    def on_items(self, *args):
        self.clear_widgets()

        for item in self.items[:10]:
            self.add_widget(EmojiButton(item))


class SvgWidget(Scatter):

    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)

        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False

        with self.canvas:
            svg = Svg(filename, bezier_points=128, circle_points=128)

        self.size = svg.width, svg.height


class EmojiButton(Button):

    font_size = 20
    size_hint = (None, None)

    def __init__(self, emoji, **kwargs):
        super(EmojiButton, self).__init__(**kwargs)

        self.size = 50, 50
        self.bind(pos=self._update_svg)

        self.svg = SvgWidget(emoji['path'], size_hint = (None, None))
        self.add_widget(self.svg)
        self.svg.scale = 0.5

    def _update_svg(self, instance, value):
        self.svg.center = instance.x + 25, instance.y + 25


class EmojiKeyboardApp(App):

    def build(self):
        return EmojiKeyboard()


if __name__ == '__main__':
    Window.size = (480, 360)
    EmojiKeyboardApp().run()
