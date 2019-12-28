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

WINDOW_WIDTH = 420
WINDOW_HEIGH = 280
BACKGROUND_COLOR = 0.15, 0.15, 0.15, 1

# TODO: Make a scrolling selection and use categories instead of limiting
MAX_FILTERED_RESULTS = 28

# TODO: Convert into preferences
CLOSE_ON_SELECTION = True
CYCLE_WITH_ARROW_KEYS = True
ICONS_PER_ROW = 7

class EmojiKeyboard(BoxLayout):

    orientation = 'vertical'
    spacing = 5
    padding = 5, 5, 5, 5

    def __init__(self, **kwargs):
        super(EmojiKeyboard, self).__init__(**kwargs)

        self.emoji_dictionary = EmojiDictionary()

        self.emoji_grid = EmojiGrid()
        self.filterInput = EmojiSearchInput(
            self.emoji_grid.hover_next_emoji,
            self.emoji_grid.hover_previous_emoji)
        self.filterInput.focus = True
        self.filterInput.bind(
            text=self.on_filter_text,
            on_text_validate=self.on_enter)

        self.add_widget(self.filterInput)
        self.add_widget(self.emoji_grid)


    def on_filter_text(self, instance, value):
        self.emoji_grid.items = self.emoji_dictionary.search(
            value, max_items=MAX_FILTERED_RESULTS)

    def on_enter(self, instance):
        self.emoji_grid.select_hovered_emoji()


class EmojiSearchInput(TextInput):
    multiline = False

    def __init__(self, hover_next_emoji, hover_previous_emoji, **kwargs):
        super(EmojiSearchInput, self).__init__(**kwargs)

        self.height = 35
        self.font_size = 18
        self.size_hint_y = None

        self.hover_next_emoji = hover_next_emoji
        self.hover_previous_emoji = hover_previous_emoji

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if CYCLE_WITH_ARROW_KEYS:
            if keycode[1] == 'up':
                self.hover_previous_emoji(row=True)
            if keycode[1] == 'down':
                self.hover_next_emoji(row=True)
                return True
            if keycode[1] == 'left':
                self.hover_previous_emoji()
                return True
            if keycode[1] == 'right':
                self.hover_next_emoji()
                return True

        if keycode[1] == 'tab':
            if 'shift' in modifiers:
                self.hover_previous_emoji()
                return True
            else:
                self.hover_next_emoji()
                return True

        if keycode[1] == 'escape':
            quit

        super().keyboard_on_key_down(window, keycode, text, modifiers)


class EmojiGrid(StackLayout):

    items = ListProperty([])
    spacing = (10, 10)

    def __init__(self, **kwargs):
        super(EmojiGrid, self).__init__(**kwargs)

        self.widgets = []
        self.hover_index = 0

    def on_items(self, *args):
        self.clear_widgets()

        def item_to_widget(item):
            return EmojiButton(item)

        self.widgets = list(map(item_to_widget, self.items))
        for widget in self.widgets:
            self.add_widget(widget)
        if len(self.widgets) > 0:
            self.hover_emoji(0)

    def select_hovered_emoji(self):
        self.widgets[self.hover_index].on_release()

    def hover_emoji(self, index):
        for widget in self.widgets:
            widget.unhover()

        self.hover_index = index
        self.widgets[index].hover()

    def hover_next_emoji(self, row=False):
        if row:
            self.hover_emoji((self.hover_index + ICONS_PER_ROW) % len(self.widgets))
        else:
            self.hover_emoji((self.hover_index + 1) % len(self.widgets))

    def hover_previous_emoji(self, row=False):
        if row:
            self.hover_emoji((self.hover_index - ICONS_PER_ROW) % len(self.widgets))
        else:
            self.hover_emoji((self.hover_index - 1) % len(self.widgets))


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

    def unhover(self):
        self.background_color = 0, 0, 0, 0

    def on_release(self):
        emoji_code = self.emoji['emoji']

        if '-' in emoji_code:
            sequence = emoji_code.split('-')
            emoji_character = chr(
                int(sequence[0], 16)) + chr(int(sequence[1], 16))
        else:
            emoji_character = chr(int(emoji_code, 16))

        Clipboard.copy(emoji_character)

        if CLOSE_ON_SELECTION:
            exit()


class EmojiKeyboardApp(App):
    title = 'Emoji Picker'

    def build(self):
        return EmojiKeyboard()


if __name__ == '__main__':
    Window.size = (WINDOW_WIDTH, WINDOW_HEIGH)
    Window.clearcolor = BACKGROUND_COLOR
    EmojiKeyboardApp().run()
