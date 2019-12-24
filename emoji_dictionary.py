
import os
import sys
import json

from collections import OrderedDict

EMOJI_MODIFIER_BASE = {
  '1f590', '1f468', '1f46e', '1f595', '1f3c3', '1f935', '1f646', '1f449',
  '1f477', '1f91c', '1f486', '1f6b6', '1f919', '1f930', '1f44b', '1f933',
  '1f6b5', '270b', '1f483', '1f64b', '1f470', '270a', '1f443', '1f918',
  '1f448', '1f471', '1f474', '1f467', '26f9', '1f44f', '1f93e', '1f6cc',
  '1f481', '1f485', '1f4aa', '1f596', '1f47c', '1f487', '1f44c', '1f476',
  '261d', '1f934', '1f385', '270c', '1f3c4', '1f64f', '1f645', '1f91e',
  '1f926', '270d', '1f647', '1f3c2', '1f6a3', '1f574', '1f3cc', '1f44a',
  '1f57a', '1f3ca', '1f450', '1f442', '1f91a', '1f93d', '1f472', '1f64d',
  '1f482', '1f3c7', '1f64c', '1f6b4', '1f938', '1f3cb', '1f936', '1f44d',
  '1f469', '1f937', '1f64e', '1f91b', '1f478', '1f447', '1f466', '1f44e',
  '1f575', '1f446', '1f6c0', '1f473', '1f939', '1f475', '1f93c'}


class EmojiDictionary:

  def __init__(self):
    self.emoji = self.__load()


  def search(self, search_term, max_items=None):
    term = search_term.lower()

    if term:
      matches = []
      for emoji in self.emoji:
        if term in emoji['description']:
          matches.append(emoji)

          if max_items and len(matches) >= max_items:
            break

      return matches
    else:
      if max_items:
        return self.emoji[:max_items]
      else:
        return self.emoji


  def __load(self):

      with open(os.path.join(os.path.dirname(__file__), 'emoji.json')) as emoji_json:
        emoji_raw = json.loads(
          emoji_json.read(), object_pairs_hook=OrderedDict)

      emojis = []

      base_props = {}
      for emoji in emoji_raw:
        category = emoji_raw[emoji]['category']
        if emoji in EMOJI_MODIFIER_BASE:
          base_props[emoji] = emoji_raw[emoji]

        if '-' in emoji:
          main_codepoint = emoji.split('-')[0]

          if main_codepoint in EMOJI_MODIFIER_BASE:
            shortname = base_props[main_codepoint]['shortname']
            description = (base_props[main_codepoint]['name']
                    + '. Keywords:'
                    + ' '.join(
                      base_props[main_codepoint]['keywords']))
          else:
            shortname = emoji_raw[emoji]['shortname']
            description = (emoji_raw[emoji]['name']
                    + '. Keywords: '
                    + ' '.join(emoji_raw[emoji]['keywords']))
        else:
          shortname = emoji_raw[emoji]['shortname']
          description = (emoji_raw[emoji]['name']
                  + '. Keywords: '
                  + ' '.join(emoji_raw[emoji]['keywords']))

        path = os.path.join(
            os.path.dirname(__file__),
            'emojitwo/png/' +
            emoji + '.png')

        if os.access(path, os.F_OK):
          emojis.append({
            'path': path,
            'name': shortname,
            'category': category,
            'emoji': emoji,
            'description': description
          })

      return emojis
