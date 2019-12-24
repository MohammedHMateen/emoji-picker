#!/usr/bin/env python3

from emoji_dictionary import EmojiDictionary

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scatter import Scatter
from kivy.uix.image import AsyncImage


class EmojiKeyboard(BoxLayout):

    search_filter = ''
    orientation = 'vertical'
    spacing = 20

    def __init__(self, **kwargs):
        super(EmojiKeyboard, self).__init__(**kwargs)

        self.emoji_dictionary = EmojiDictionary()

        self.emoji_grid = EmojiGrid()
        self.filterInput = TextInput(multiline=False, size_hint_y=None, height=40)
        self.filterInput.focus = True
        self.filterInput.bind(text=self.on_filter_text)

        self.add_widget(self.filterInput)
        self.add_widget(self.emoji_grid)

    def on_filter_text(self, instance, value):
        self.emoji_grid.items = self.emoji_dictionary.search(
            value, max_items=50)


class EmojiGrid(StackLayout):

    items = ListProperty([])
    spacing = (20, 20)

    def __init__(self, **kwargs):
        super(EmojiGrid, self).__init__(**kwargs)

    def on_items(self, *args):
        self.clear_widgets()

        for item in self.items:
            self.add_widget(EmojiButton(item))


class EmojiButton(Button):

    font_size = 20
    size_hint = (None, None)

    def __init__(self, emoji, **kwargs):
        super(EmojiButton, self).__init__(**kwargs)
        self.emoji = emoji

        self.image = AsyncImage(source=emoji['path'])
        self.add_widget(self.image)

        self.bind(size=self._update_image, pos=self._update_image)
        self.size = 50, 50

    def _update_image(self, instance, value):
        self.image.center = instance.center
        self.image.size = 40, 40

    def on_release(self):
        emoji_code = self.emoji['emoji']

        if '-' in emoji_code:
            sequence = emoji_code.split('-')
            emoji_character = chr(int(sequence[0], 16)) + chr(int(sequence[1], 16))
        else:
            emoji_character = chr(int(emoji_code, 16))

        Clipboard.copy(emoji_character)
        exit()


class EmojiKeyboardApp(App):

    def build(self):
        return EmojiKeyboard()


if __name__ == '__main__':
    Window.size = (480, 360)
    EmojiKeyboardApp().run()
