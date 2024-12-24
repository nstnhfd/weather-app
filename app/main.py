from fastapi import HTTPException
import requests  
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from form import Ui_MainWindow
import sys
import requests
class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)  
        self.setWindowTitle("Weather")  
        self.ui.new_city.clicked.connect(self.get_weather) 

        in_city = self.current_loc()
        self.ui.new_city.setDisabled(True)             
        self.ui.pln.setPlainText(in_city)
        self.get_weather()
        self.ui.pln.textChanged.connect(self.enable_button)
        self.ui.new_city.clicked.connect(lambda:self.get_weather)
         
    def get_weather(self):                   
        param1 = self.ui.pln.toPlainText()               
        # Prepare payload for the request  
        payload = {  
            "param1": param1,              
        }          
        # Send POST request to FastAPI  
        try:  
            response = requests.post('http://127.0.0.1:8000/setparams', json=payload)              
            if response.status_code == 200:      
                weather_data = response.json()  
                main = weather_data['params']['main']  
                weather = weather_data['params']['weather'][0]  # Get the first weather condition  
                location = weather_data['params']['name']  
                params = weather_data['params']
                coordinates = weather_data['params']['coord']  
                latitude = coordinates['lat']  
                longitude = coordinates['lon']
                sunrise_time = weather_data['params']['sys']['sunrise']  


                self.ui.lbltemprature.setText(f"{main['temp']}") 

                 
                self.ui.lbltemp.setText(f"{main['humidity']}%")  
                self.ui.status.setText(f"{weather['description']}")  
                
              
                self.ui.lbllat.setText(f"{latitude}")  
                self.ui.lbllot.setText(f"{longitude}")  
                
                self.ui.mintemp.setText(f"{main['temp_min']}°C")
                self.ui.maxtemp.setText(f"{main['temp_max']}°C")

                self.ui.lblwinds.setText(f"{params['wind']['speed']} m/s")  
                self.ui.lblpressure.setText(f"{main['pressure']} hPa")  
                self.ui.lblsunrise.setText(f"{sunrise_time}")  

                
            else:
                QMessageBox.critical(self, "Error", f"Request failed with status code: {response.status_code}. Response: {response.text}")  
        except requests.exceptions.RequestException as e:  
            QMessageBox.critical(self, "Error", f"Request failed: {e}")  
    def current_loc(self):
        ip_req  = requests.get('https://get.geojs.io/v1/ip.json')
        my_ip = ip_req.json()['ip']
        url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
        geo_req = requests.get(url)
        geo_res = geo_req.json()
        timez2 = geo_res['timezone']
        city = timez2.split('/')[1]
        return (city)
    def enable_button(self):
       self.ui.new_city.setDisabled(False)

def main():
    app=QApplication(sys.argv)
    app.setApplicationName("weather")
    app.setApplicationVersion("1.0")
    win=Window()
    win.show()
    sys.exit(app.exec_())    
main()
