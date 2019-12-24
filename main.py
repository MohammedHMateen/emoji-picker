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

MAX_FILTERED_RESULTS = 28
WINDOW_WIDTH = 420
WINDOW_HEIGH = 280

# TODO: Convert into preferences
CLOSE_ON_SELECTION = True

class EmojiKeyboard(BoxLayout):

    orientation = 'vertical'
    spacing = 5
    padding = 5, 5, 5, 5

    def __init__(self, **kwargs):
        super(EmojiKeyboard, self).__init__(**kwargs)

        self.emoji_dictionary = EmojiDictionary()

        self.emoji_grid = EmojiGrid()
        self.filterInput = TextInput(multiline=False, size_hint_y=None, height=35)
        self.filterInput.focus = True
        self.filterInput.font_size = 18
        self.filterInput.bind(text=self.on_filter_text, on_text_validate=self.on_enter)

        self.add_widget(self.filterInput)
        self.add_widget(self.emoji_grid)

    def on_filter_text(self, instance, value):
        print(value)
        self.emoji_grid.items = self.emoji_dictionary.search(
            value, max_items=MAX_FILTERED_RESULTS)

    def on_enter(self, instance):
        self.emoji_grid.select_hovered_emoji()


class EmojiGrid(StackLayout):

    items = ListProperty([])
    spacing = (10, 10)

    def __init__(self, **kwargs):
        super(EmojiGrid, self).__init__(**kwargs)

    def on_items(self, *args):
        self.clear_widgets()

        def item_to_widget(item):
            return EmojiButton(item)

        widgets = list(map(item_to_widget, self.items))
        for widget in widgets:
            self.add_widget(widget)
        if len(widgets) > 0:
            widgets[0].hover()
            self.selected_widget = widgets[0]

    def select_hovered_emoji(self):
        self.selected_widget.on_release()


class EmojiButton(Button):

    size_hint = (None, None)

    def __init__(self, emoji, selected=False, **kwargs):
        super(EmojiButton, self).__init__(**kwargs)

        self.emoji = emoji
        self.selected = selected

        self.image = AsyncImage(source=emoji['path'])
        self.add_widget(self.image)

        self.bind(size=self._update_image, pos=self._update_image)
        self.size = 50, 50
        self.background_color = 0, 0, 0, 0

    def _update_image(self, instance, value):
        self.image.center = instance.center
        self.image.size = 35, 35

    def hover(self):
        self.background_color = 1, 1, 1, 0.5

    def on_release(self):
        emoji_code = self.emoji['emoji']

        if '-' in emoji_code:
            sequence = emoji_code.split('-')
            emoji_character = chr(int(sequence[0], 16)) + chr(int(sequence[1], 16))
        else:
            emoji_character = chr(int(emoji_code, 16))

        Clipboard.copy(emoji_character)

        if CLOSE_ON_SELECTION:
            exit()


class EmojiKeyboardApp(App):

    def build(self):
        return EmojiKeyboard()


if __name__ == '__main__':
    Window.size = (WINDOW_WIDTH, WINDOW_HEIGH)
    Window.clearcolor = 0.15, 0.15, 0.15, 1
    EmojiKeyboardApp().run()
