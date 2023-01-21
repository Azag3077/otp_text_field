from kivy.clock import Clock
from kivy.core.text import DEFAULT_FONT
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty, \
    ColorProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

Builder.load_string("""
#: import get_color_from_hex kivy.utils.get_color_from_hex
<OTPLabel>:
    size_hint: None, None
    size: self.widget_parent.box_size
    color: self.widget_parent.text_color
    font_size: self.widget_parent.font_size
    font_name: self.widget_parent.font_name
    bold: True
    cursor_active: False

    canvas.before:
        Color:
            rgba: self.widget_parent.border_secondary_active_color[:3] + [1 if self.widget_parent.focus_widget == self else 0]
        Line:
            width: self.widget_parent.focus_line_active
            rounded_rectangle:
                self.x - self.widget_parent.focus_line_active, self.y - self.widget_parent.focus_line_active, \
                self.width + self.widget_parent.focus_line_active*2, self.height + self.widget_parent.focus_line_active*2, \
                self.widget_parent.radius

        Color:
            rgba: self.widget_parent.border_primary_active_color \
                  if self.widget_parent.focus_widget == self else \
                  self.widget_parent.border_inactive_color
        Line:
            width: self.widget_parent.focus_line_inactive if self.widget_parent.focus_widget == self else dp(.7)
            rounded_rectangle:
                self.x - self.widget_parent.focus_line_inactive, self.y - self.widget_parent.focus_line_inactive, \
                self.width + self.widget_parent.focus_line_inactive*2, self.height + self.widget_parent.focus_line_inactive*2, \
                self.widget_parent.radius
                
        Color:
            rgba: self.widget_parent.cursor_color[:3] + [1 if self.cursor_active else 0]
        Line:
            cap: "square"
            width: self.widget_parent.cursor_width
            points: self.center_x, self.y + self.height * .25, self.center_x, self.y + self.height * .75,

""")

Builder.load_string("""
<OTPInputField>:
    size_hint: None, None
    size: box.width + self.focus_line_active*2, box.height + self.focus_line_active*2

    BoxLayout:
        id: box
        spacing: root.spacing
        size_hint: None, None
        size: self.minimum_size
        pos: root.x + root.focus_line_active/2, root.y + root.focus_line_active/2

    TextInput:
        id: field
        opacity: 0
        font_size: 0
        pos: root.pos
        size: root.size
        multiline: False
        use_handles: False
        input_filter: "int"
        input_type: "number"
        size_hint: None, None
        on_focus: root.on_focus()
        on_text: root.on_textedit()
        on_text_validate: root.dispatch("on_validate")

""")


class OTPLabel(Label):
    widget_parent = ObjectProperty()

    def __init__(self, **kwargs):
        super(OTPLabel, self).__init__(**kwargs)


class OTPInputField(FloatLayout):
    """OTPInputField class.

    :Events:
        `on_validate`
            Fired when the user hits 'enter'.
            This will unfocus the textinput.
        `on_complete`
            Fired when the InputField has been filled.
    """

    __events__ = ("on_validate", "on_complete")

    text_color = ColorProperty(get_color_from_hex('#616161'))
    '''Current color of the text, in (r, g, b, a) format.

    :attr:`text_color` is a :class:`~kivy.properties.ColorProperty` and
    defaults to [97/255, 97/255, 97/255, 1]
    '''

    border_primary_active_color = ColorProperty(get_color_from_hex('#1E88E5'))
    '''Current color of the primary border when active, in (r, g, b, a) format.

    :attr:`text_color` is a :class:`~kivy.properties.ColorProperty` and
    defaults to [68/255, 138/255, 1, 1].
    '''

    border_secondary_active_color = ColorProperty(get_color_from_hex('#BBDEFB'))
    '''Current color of the secondary border when active, in (r, g, b, a) format.

    :attr:`border_secondary_active_color` is a :class:`~kivy.properties.ColorProperty` and
    defaults to [68/255, 138/255, 1, 1].
    '''

    border_inactive_color = ColorProperty(get_color_from_hex('#616161'))
    '''Current color of the border when not focused, in (r, g, b, a) format.

    :attr:`border_inactive_color` is a :class:`~kivy.properties.ColorProperty` and
    defaults to [97/255, 97/255, 97/255, 1] same as the default text_color.
    '''

    spacing = NumericProperty('12dp')
    '''The spacing between the boxes

    :attr:`spacing` is a :class:`~kivy.properties.NumericProperty`
    adn defaults 12.
    '''

    auto_focus = BooleanProperty()
    '''If True, will focus the field intput and bring up the keyboard
    at the very first time it is shown on the screen.

    :attr:`auto_focus` is a :class:`~kivy.properties.BooleanProperty`
    adn defaults True.
    '''

    radius = NumericProperty('4dp')
    '''The border radius for bot the primary and secondary border.

    :attr:`radius` is a :class:`~kivy.properties.NumericProperty`
    adn defaults 4.
    '''

    font_size = NumericProperty('20sp')
    '''Font size of the text in pixels.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 20 :attr:`~kivy.metrics.sp`.
    '''

    font_name = StringProperty(DEFAULT_FONT)
    '''Filename of the font to use. The path can be absolute or relative.
    Relative paths are resolved by the :func:`~kivy.resources.resource_find`
    function.

    :attr:`font_name` is a :class:`~kivy.properties.StringProperty` and
    defaults to 'Roboto'. This value is taken
    from :class:`~kivy.config.Config`.
    '''

    cursor_width = NumericProperty('1sp')
    '''Current width of the cursor.

    :attr:`cursor_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to '1sp'.
    '''

    cursor_color = ColorProperty([1, 0, 0, 1])
    '''Current color of the cursor, in (r, g, b, a) format.

    :attr:`cursor_color` is a :class:`~kivy.properties.ColorProperty` and
    defaults to [1, 0, 0, 1].
    '''

    length = NumericProperty(6)
    '''Length of text of the input field.
    The preferable length should be in range of 3 and 6.
    More than 6 may display the widget beyond the screen 

    :attr:`length` is a :class:`~kivy.properties.NumericProperty` and
    defaults to '6'.
    '''

    text = StringProperty()
    box_size = ListProperty([0, 0])
    focus_line_active = NumericProperty('3.5dp')
    focus_line_inactive = NumericProperty('1.3dp')
    focus_widget = ObjectProperty(allownone=True)

    clock = None

    def __init__(self, **kwargs):
        super(OTPInputField, self).__init__(**kwargs)
        Clock.schedule_once(lambda x: self.update(), .1)

    def on_validate(self):
        pass

    def on_complete(self):
        pass

    def update(self):
        for i in range(self.length):
            self.ids.box.add_widget(OTPLabel(widget_parent=self))

        self.check_size()
        self.ids.field.focus = self.auto_focus
        self.parent.bind(size=lambda *x: self.check_size())
        self.blink_cursor(0)

    def blink_cursor(self, index):
        for wid in self.ids.box.children:
            wid.cursor_active = False

        if self.clock:
            self.clock.cancel()

        wid = self.ids.box.children[self.length-1 - index]
        wid.cursor_active = True

        self.clock = Clock.schedule_interval(lambda x: self.schedule_blink(index), .5)

    def schedule_blink(self, index):
        wid = self.ids.box.children[self.length-1 - index]
        value = wid.cursor_active
        wid.cursor_active = not value

    def cancel_blink(self):
        for wid in self.ids.box.children:
            wid.cursor_active = False

        if self.clock:
            self.clock.cancel()

    def check_size(self):
        if self.width < self.parent.width:
            self.box_size = dp(35), dp(48)
            self.focus_line_active = dp(3.5)
            self.focus_line_inactive = dp(1.3)
            return

        wid = (self.parent.width - dp(12 * self.length-1 + 15 * 2)) / self.length
        self.box_size = wid, dp(48)

    def on_focus(self):
        if not self.ids.field.focus:
            self.focus_widget = None
            self.cancel_blink()
            return

        self.focus_current()

    def on_textedit(self):
        self.focus_current()
        self.text = self.ids.field.text = self.ids.field.text[:self.length]

        if len(self.ids.field.text) == self.length:
            self.ids.field.focus = False
            self.focus_widget = None
            self.dispatch("on_complete")
            return

    def focus_current(self):
        index = min(self.length-1, len(self.ids.field.text))
        self.blink_cursor(index)
        wid = self.ids.box.children[self.length-1 - index]
        self.focus_widget = wid

        texts = self.ids.field.text.ljust(self.length)
        widgets = reversed(self.ids.box.children.copy())

        for text, wid in zip(texts, widgets):
            wid.text = text


kv = """
Screen:
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'center_y': .5}
        
        Label:
            text: "Enter the code sent to your phone."
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: dp(5)
            color: 0, 0, 0
        
        OTPInputField:
            pos_hint: {'center_x': .5}
            on_text: app.on_text(self)
            on_complete: app.on_complete(self)
            on_validate: app.on_validate(self)
"""


class Example(App):
    def build(self):
        return Builder.load_string(kv)

    def on_focus(self, instance):  # NOQA
        print('[callback]...on_focus')
        print(f'[instance]...{instance}')
        print(f'[value]......{instance.focus}')
        print()

    def on_text(self, instance):  # NOQA
        print('[callback]...on_text')
        print(f'[instance]...{instance}')
        print(f'[value]......{instance.text}')
        print()

    def on_validate(self, instance):  # NOQA
        print(f'[on_validate] {instance}')

    def on_complete(self, instance):  # NOQA
        print(f'[on_complete] {instance}')


if __name__ == '__main__':
    Example().run()
