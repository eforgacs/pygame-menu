"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET ADDITION EXAMPLE DOCS
See https://pygame-menu.readthedocs.io/en/latest/_source/add_widgets.html

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import sys

sys.path.insert(0, '../')

import pygame
import pygame_menu
from typing import List

# Init pygame
pygame.init()
surface = pygame.display.set_mode((400, 300))
pygame.display.set_caption('pygame-menu v4')

# Set pygame-menu image
icon = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU).get_surface()
pygame.display.set_icon(icon)

# Set example, only this should change
EXAMPLE = 'DROPSELECT'

# Create example
menu: 'pygame_menu.Menu'
widgets: List['pygame_menu.widgets.Widget']


def make_menu(menu_theme: 'pygame_menu.themes.Theme', title: str,
              widget_font_size: int = 25) -> 'pygame_menu.Menu':
    """
    Make menu.

    :param menu_theme: Menu theme object
    :param title: Menu title
    :param widget_font_size: Theme widget font size
    :return: Menu object
    """
    menu_theme = menu_theme.copy()
    menu_theme.title_font_size = 35
    menu_theme.widget_font_size = widget_font_size

    return pygame_menu.Menu(
        column_min_width=400,
        height=300,
        theme=menu_theme,
        title=title,
        onclose=pygame_menu.events.CLOSE,
        width=400
    )


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
def change_background_color(selected_value, color, **kwargs):
    from random import randrange
    value_tuple, index = selected_value
    print('Change widget color to', value_tuple[0])  # selected_value format ('Color', surface, color)
    if color == (-1, -1, -1):  # Generate a random color
        color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    widget: 'pygame_menu.widgets.Selector' = kwargs.get('widget')
    widget.update_font({'selected_color': color})
    widget.get_selection_effect().color = color


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
def func(name):
    print('Hello world from', name)  # name will be 'foo'


if EXAMPLE == 'BUTTON':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Button')
    about_menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'About')
    menu.add.button('Exec', func, 'foo',  # Execute a function, it receives 'foo' as *arg
                    align=pygame_menu.locals.ALIGN_LEFT)
    btn = menu.add.button(about_menu.get_title(), about_menu,  # Open a sub-menu
                          shadow=True, shadow_color=(0, 0, 100))
    menu.add.button('Exit', pygame_menu.events.EXIT,  # Link to exit action
                    align=pygame_menu.locals.ALIGN_RIGHT)
    btn.select(update_menu=True)

elif EXAMPLE == 'COLORINPUT':
    menu = make_menu(pygame_menu.themes.THEME_DARK, 'Color Entry')
    menu.add.color_input('RGB color 1: ', color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB,
                         default=(255, 0, 255), font_size=18)
    menu.add.color_input('RGB color 2: ', color_type=pygame_menu.widgets.COLORINPUT_TYPE_RGB,
                         input_separator='-', font_size=18)
    menu.add.color_input('HEX color 3: ', color_type=pygame_menu.widgets.COLORINPUT_TYPE_HEX,
                         default='#ffaa11', font_size=18)

elif EXAMPLE == 'DROPSELECT':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Drop Select')
    selector_epic = menu.add.dropselect(
        title='Is pygame-menu epic?',
        items=[('Yes', 0),
               ('Absolutely Yes', 1)],
        font_size=16,
        selection_option_font_size=20
    )
    selector_sum = menu.add.dropselect(
        title='What is the value of π?',
        items=[('3 (Engineer)', 0),
               ('3.141592653589793238462643383279502884197169399375105820974944592', 1),
               ('4', 2),
               ('I don\'t know what is π', 3)],
        font_size=16,
        selection_box_width=173,
        selection_option_padding=(0, 5),
        selection_option_font_size=20
    )
    selector_country = menu.add.dropselect(
        title='Pick a country',
        items=[('Argentina', 'ar'),
               ('Australia', 'au'),
               ('Bolivia', 'bo'),
               ('Chile', 'ch'),
               ('China', 'cn'),
               ('Finland', 'fi'),
               ('France', 'fr'),
               ('Germany', 'de'),
               ('Italy', 'it'),
               ('Japan', 'jp'),
               ('Mexico', 'mx'),
               ('Peru', 'pe'),
               ('United States', 'us')],
        font_size=20,
        default=3,
        open_middle=True,  # Opens in the middle of the menu
        selection_box_height=5,
        selection_box_width=212,
        selection_infinite=True,
        selection_option_font_size=20
    )

elif EXAMPLE == 'FRAME':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Frames', widget_font_size=18)
    menu.get_theme().widget_selection_effect.zero_margin()
    frame = menu.add.frame_v(250, 150, background_color=(50, 50, 50))
    frame_title = menu.add.frame_h(250, 29, background_color=(180, 180, 180))
    frame_content = menu.add.frame_v(250, 120)
    frame.pack(frame_title)
    frame.pack(frame_content)

    frame_title.pack(menu.add.label('Settings'), margin=(2, 2))
    frame_title.pack(
        menu.add.button('Close', pygame_menu.events.EXIT, padding=(0, 5), background_color=(100, 100, 100)),
        alignment=pygame_menu.locals.ALIGN_RIGHT, margin=(-2, 2))
    frame_content.pack(menu.add.label('Pick a number', font_color=(150, 150, 150)),
                       alignment=pygame_menu.locals.ALIGN_CENTER)
    frame_numbers = menu.add.frame_h(250, 41)
    frame_content.pack(frame_numbers)
    for i in range(9):
        frame_numbers.pack(menu.add.button(i, font_color=(5 * i, 11 * i, 13 * i), padding=(0, 5), font_size=30),
                           alignment=pygame_menu.locals.ALIGN_CENTER)
    frame_content.pack(menu.add.vertical_margin(15))
    frame_content.pack(menu.add.toggle_switch('Nice toggle', False, width=100, font_color=(150, 150, 150)),
                       alignment=pygame_menu.locals.ALIGN_CENTER)

elif EXAMPLE == 'IMAGE':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Image')
    image_path = pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    menu.add.image(image_path, angle=10, scale=(0.15, 0.15))
    menu.add.image(image_path, angle=-10, scale=(0.15, 0.15))

elif EXAMPLE == 'LABEL':
    menu = make_menu(pygame_menu.themes.THEME_BLUE, 'Label')
    HELP = "Press ESC to enable/disable Menu " \
           "Press ENTER to access a Sub-Menu or use an option " \
           "Press UP/DOWN to move through Menu " \
           "Press LEFT/RIGHT to move through Selectors."
    menu.add.label(HELP, max_char=-1, font_size=20)

elif EXAMPLE == 'SELECTOR':
    menu = make_menu(pygame_menu.themes.THEME_ORANGE, 'Selector')
    items = [('Default', (255, 255, 255)),
             ('Black', (0, 0, 0)),
             ('Blue', (0, 0, 255)),
             ('Random', (-1, -1, -1))]
    selector = menu.add.selector(
        title='Current color:\t',
        items=items,
        onreturn=change_background_color,  # user press "Return" button
        onchange=change_background_color  # User changes value with left/right keys
    )
    selector.add_self_to_kwargs()  # callbacks will receive widget as parameter
    selector2 = menu.add.selector(
        title='New color:',
        items=items,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
    )

elif EXAMPLE == 'TEXTINPUT':
    menu = make_menu(pygame_menu.themes.THEME_GREEN, 'Text Entry')
    menu.add.text_input('First name: ', default='John')
    menu.add.text_input('Last name: ', default='Doe', maxchar=10, input_underline='_')
    menu.add.text_input('Password: ', input_type=pygame_menu.locals.INPUT_INT, password=True)

elif EXAMPLE == 'TOGGLESWITCH':
    menu = make_menu(pygame_menu.themes.THEME_SOLARIZED, 'Switches')
    menu.add.toggle_switch('First Switch', False, toggleswitch_id='first_switch')
    menu.add.toggle_switch('Other Switch', True, toggleswitch_id='second_switch',
                           state_text=('Apagado', 'Encencido'), state_text_font_size=18)

elif EXAMPLE == 'URL':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Url', widget_font_size=18)
    menu.add.url('https://github.com/ppizarror/pygame-menu')
    menu.add.url('https://github.com/ppizarror/pygame-menu', 'The best menu ever')
    menu.add.url('https://pygame-menu.readthedocs.io/en/master/', 'pygame-menu documentation')

elif EXAMPLE == 'VERTICALMARGIN':
    menu = make_menu(pygame_menu.themes.THEME_DEFAULT, 'Vertical spacer')
    menu.add.label('Text #1')
    menu.add.vertical_margin(100)
    menu.add.label('Text #2')

else:
    raise ValueError('unknown example "{}"'.format(EXAMPLE))

# Execute menu
menu.mainloop(surface)
