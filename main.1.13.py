import kivy
from os.path import join, dirname
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

kivy.require('1.0.6')

class Picture(Scatter):
    source = StringProperty(None)
    
class ScrollableList(RelativeLayout):
    def __init__(self, images=None, **kwargs):
        super(ScrollableList, self).__init__(**kwargs)
        self.images = images

        # Top left corner label
        label_Vlad = Label(text='FishFarmFinder\nby Vlad Iljin', size_hint=(None, None), size=(100, 50), pos_hint={'top': 1, 'right': 1}, font_size=9)
        self.add_widget(label_Vlad)

        # Top Area with a label and an image
        top_area = BoxLayout(size_hint=(1, 0.5), height=50)

        # Top left corner image
        image = Image(source='data/image1.png', size_hint=(None, None), size=(100, 50))
        top_area.add_widget(image)

        # Create a BoxLayout to hold the list of buttons
        self.list_layout = BoxLayout(orientation='vertical', spacing=1, size_hint_y=None, padding=20)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))

        # Create buttons with names from SiteList and add them to the list
        for site_name in SiteList:
            btn = Button(text=site_name, size_hint_y=None, height=50)
            btn.bind(on_release=self.on_button_click)
            self.list_layout.add_widget(btn)

        # Create a ScrollView to scroll the list
        self.scroll_view = ScrollView(size_hint=(1, 0.5))
        self.scroll_view.add_widget(self.list_layout)

        # Add the top area and the ScrollView to the RelativeLayout
        self.add_widget(top_area)
        self.add_widget(self.scroll_view)

        # Exit Button overlaid on top of the Top Area
        exit_button = Button(text='Exit', size_hint=(None, None), size=(70, 50), pos=(10, self.height + 630))
        exit_button.bind(on_release=self.show_exit_popup)
        self.add_widget(exit_button)

        # Bind the property change event
        self.scroll_view.bind(scroll_y=self.on_scroll)

    def on_button_click(self, instance):
        # Create the content of the popup
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Button '{instance.text}' clicked!"))

        # Display the corresponding image
        if instance.text in self.images:
            image_widget = Image(texture=self.images[instance.text].texture)
            content.add_widget(image_widget)

        # Create the OK button to close the popup, taking entire width
        ok_button = Button(text='OK', size_hint=(1, None), height=50)
        ok_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(ok_button)

        # Create the popup window
        popup = Popup(title='Button Clicked',
                      content=content,
                      size_hint=(None, None),
                      size=(480, 800))

        # Open the popup
        popup.open()

    def show_exit_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to exit?'))

        yes_button = Button(text='Yes', on_release=self.exit_app)
        no_button = Button(text='No', on_release=self.dismiss_popup)

        buttons_layout = BoxLayout()
        buttons_layout.add_widget(yes_button)
        buttons_layout.add_widget(no_button)

        content.add_widget(buttons_layout)

        popup = Popup(title='Exit Confirmation',
                      content=content,
                      size_hint=(None, None), size=(300, 150))
        popup.open()

    def exit_app(self, instance):
        App.get_running_app().stop()

    def dismiss_popup(self, instance):
        instance.parent.parent.dismiss()

    def on_scroll(self, instance, value):
        # Calculate the position of the top visible button
        top_button_index = int((value * (len(SiteList) - 1)) + 0.5)

        # Check if the index is within the bounds of the list
        if 0 <= top_button_index < len(self.list_layout.children):
            top_button = self.list_layout.children[top_button_index]
            print(f"Top Button: {top_button.text}")

class MyApp(App):
    def preload_images(self):
        # Load all images into memory here
        self.images = {}
        for site_name in SiteList:
            image_path = f'data/{site_name}.png'  # Adjust the path as per your file structure
            try:
                self.images[site_name] = CoreImage(image_path)
            except Exception as e:
                print(f"Error loading image '{site_name}': {e}")

    def build(self):
        # Preload images when the app starts
        self.preload_images()
        
        return ScrollableList(images=self.images)

if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'width', '480')
    Config.set('graphics', 'height', '800')

    SiteList = [
        'Airds Point',
        'An Camus',
        'Ardintoul',
        'Ardmair',
        'Ardnish',
        'Ardessey',
        'BDNC',
        'Cairidth',
        'Carradale',
        'Colonsay',
        'Duich',
        'Gorsten',
        'Greshornish',
        'Greanem',
        'Groatay',
        'Grey Horse Channel',
        'Hellisay',
        'Invasion Bay',
        'Inverawe',
        'Kingairloch',
        'Laga Bay',
        'Leven',
        'Linhe',
        'Loch Alsh',
        'Loch Hourn',
        'Loch Shell',
        'Loch Skipport',
        'MacLeans Nose',
        'Marulaig Bay',
        'Moal Ban',
        'Muck',
        'NorthShore',
        'PNG',
        'PNC',
        'Port na Mine',
        'Portnalong',
        'Rum',
        'Sailean Ruadh',
        'Sconser Quarry',
        'Scalpay',
        'Seaforth',
        'Stulaigh',
        'Sunart',
        'SW Shuna',
        'Tabhaigh',
        'Torridon',
        'Trilleachan Mor',
        'WesterRoss',
        'West Loch Tarbert',
    ]

    MyApp().run()
