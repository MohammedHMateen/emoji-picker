from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty


class EmojiKeyboard(BoxLayout):

    search_filter = ''
    orientation = 'vertical'
    spacing = 20

    def __init__(self, **kwargs):
        super(EmojiKeyboard, self).__init__(**kwargs)

        self.all_emojis = [
            ':D',
            ':)',
            ':(',
            ':|',
            ':X',
            ':3',
            ':P',
            ':C',
            '=)',
            '=D',
            '=('
        ]

        self.emoji_grid = EmojiGrid()
        self.filterInput = TextInput(multiline=False, size_hint_y=None, height=50)
        self.filterInput.focus = True
        self.filterInput.bind(text=self.on_filter_text)

        self.add_widget(self.filterInput)
        self.add_widget(self.emoji_grid)

    def filter_emoji(self, emoji):
        return self.search_filter.lower() in emoji.lower()

    def on_filter_text(self, instance, value):
        self.search_filter = value
        self.emoji_grid.items = list(filter(self.filter_emoji, self.all_emojis))


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

        self.text = emoji
        self.size = (80, 80)


class EmojiKeyboardApp(App):

    def build(self):
        return EmojiKeyboard()


if __name__ == '__main__':
    EmojiKeyboardApp().run()
