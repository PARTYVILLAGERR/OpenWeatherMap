from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
import requests

class RunApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        
        self.location_input_layout = GridLayout(cols=2, size_hint_y=None, height=44)
        
        self.location_label = Label(text="Enter Location:")
        self.text_input1 = TextInput()
        
        self.location_input_layout.add_widget(self.location_label)
        self.location_input_layout.add_widget(self.text_input1)
        
        self.spinner_layout = GridLayout(cols=2, size_hint_y=None, height=44)
        
        self.unit_label = Label(text="Temperature Unit:")
        self.temp_select = Spinner(
            text='Celsius',
            values=('Celsius', 'Fahrenheit'),
        )
        
        self.spinner_layout.add_widget(self.unit_label)
        self.spinner_layout.add_widget(self.temp_select)
        
        self.radio_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=44)
        
        self.cordinate_label = Label(text="Use Latitude and Longitude:")
        self.yes_button = ToggleButton(text="Yes", group="radio_group", state="normal")
        self.no_button = ToggleButton(text='No', group='radio_group', state='down')
        self.yes_button.bind(on_press=self.on_button_press)
        self.no_button.bind(on_press=self.on_button_press)
        
        self.radio_layout.add_widget(self.cordinate_label)
        self.radio_layout.add_widget(self.yes_button)
        self.radio_layout.add_widget(self.no_button)
        
        self.weather_button = Button(text="Get Weather Information", height=44)
        self.weather_button.bind(on_press=self.get_weather)
        
        self.window.add_widget(self.location_input_layout)
        self.window.add_widget(self.spinner_layout)
        self.window.add_widget(self.radio_layout)
        self.window.add_widget(self.weather_button)
        
        return self.window
    
    def get_weather(self, instance):
        unit = self.temp_select.text
        api_key = "55c1965a894d3b4f9248faf0236afd27"
        unit_mapping = {
            'Celsius': 'metric',
            'Fahrenheit': 'imperial'
        }
        api_unit = unit_mapping.get(unit, 'celsius')
    
        if self.no_button.state == "down":
            location = self.text_input1.text
            
            if location:
                try:
                    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units={api_unit}&appid={api_key}')
                    data = response.json()
                    
                    temp = data['main']['temp']
                    wind_speed = data['wind']['speed']
                    
                    precipitation = data.get('rain', {}).get('1h', 0)
                    if precipitation > 0:
                        precipitation_percentage = "High chance of precipitation"
                    else:
                        precipitation_percentage = "No precipitation expected"
                    
                    weather_info = (
                        f"The temperature is {temp}° in {location} ({unit}).\n"
                        f"Wind speed: {wind_speed} m/s\n"
                        f"Precipitation: {precipitation} mm"
                    )
                except Exception as e:
                    weather_info = f"An error occurred: {e}"
                    
                popup_label = Label(text=weather_info)
                popup = Popup(title="Information", content=popup_label, size_hint=(None, None), size=(400, 200))
                popup.open()
        elif self.yes_button.state == "down":
            latitude = self.lat_text_input.text
            longitude = self.long_text_input.text
            
            if latitude and longitude:
                try:
                    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units={api_unit}')
                    data = response.json()
                    
                    temp = data['main']['temp']
                    wind_speed = data['wind']['speed']
                    
                    precipitation = data.get('rain', {}).get('1h', 0)
                    precipitation_percentage = "High chance of precipitation" if precipitation > 0 else "No precipitation expected"
                    
                    weather_info = (
                        f"The temperature is {temp}° in {unit} \nlatitude: {latitude}, longitude: {longitude}.\n\n"
                        f"Wind speed: {wind_speed} m/s\n"
                        f"Precipitation: {precipitation} mm"
                    )
                    
                except Exception as e:
                    weather_info = f"An error occurred: {e}"
                
                popup_label = Label(text=weather_info)
                popup = Popup(title="Information", content=popup_label, size_hint=(None, None), size=(400, 200))
                popup.open()               
    
    def on_button_press(self, instance):
        if self.yes_button.state == "down":
            if self.location_input_layout in self.window.children:
                self.window.remove_widget(self.location_input_layout)
            
            self.cordinate_input_layout = GridLayout(cols=2, size_hint_y=None, height=88)
            
            self.lat_input_label = Label(text="Enter Latitude")
            self.long_input_label = Label(text="Enter Longitude")
            
            self.lat_text_input = TextInput()            
            self.long_text_input = TextInput()
            
            self.cordinate_input_layout.add_widget(self.lat_input_label)
            self.cordinate_input_layout.add_widget(self.lat_text_input)
            self.cordinate_input_layout.add_widget(self.long_input_label)
            self.cordinate_input_layout.add_widget(self.long_text_input)
            
            self.window.remove_widget(self.spinner_layout)
            self.window.remove_widget(self.radio_layout)
            self.window.remove_widget(self.weather_button)
            
            self.window.add_widget(self.cordinate_input_layout)
            self.window.add_widget(self.spinner_layout)
            self.window.add_widget(self.radio_layout)
            self.window.add_widget(self.weather_button)            
            
        elif self.no_button.state == "down":
            if self.location_input_layout not in self.window.children:
                if self.location_input_layout.parent:
                    self.location_input_layout.parent.remove_widget(self.location_input_layout)
                if self.cordinate_input_layout.parent:
                    self.cordinate_input_layout.parent.remove_widget(self.cordinate_input_layout)
                self.window.remove_widget(self.spinner_layout)
                self.window.remove_widget(self.radio_layout)
                self.window.remove_widget(self.weather_button)
                
                self.window.add_widget(self.location_input_layout)
                self.window.add_widget(self.spinner_layout)
                self.window.add_widget(self.radio_layout)
                self.window.add_widget(self.weather_button)
    
if __name__ == "__main__":
    RunApp().run()