import sys
import requests
import PyQt5
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
#import matplotlib.pyplot as plt
class WeatherWatcher(QWidget):
    def __init__(self):
        super().__init__()
        self.titleLabel = QLabel("Weather Watcher", self)
        self.locationLabel = QLabel("Location: ", self)
        self.locationInput = QLineEdit(self)
        self.getWeatherButton = QPushButton("Get weather", self)
        self.fullLocationLabel = QLabel(self)
        self.temperatureLabel = QLabel(self)
        self.imageLabel = QLabel(self)
        self.descriptionLabel=QLabel(self)
        self.initUI()
        
    def initUI(self):
        
        ##################################################################################################################

        self.setWindowTitle("Weather Watcher")
        self.setFixedWidth(800)
        self.setWindowIcon(QtGui.QIcon('TestIcon.png'))
        vbox = QVBoxLayout()
        vbox.addWidget(self.titleLabel)
        vbox.addWidget(self.locationLabel)
        vbox.addWidget(self.locationInput)
        vbox.addWidget(self.getWeatherButton)
        vbox.addWidget(self.fullLocationLabel)
        vbox.addWidget(self.temperatureLabel)
        vbox.addWidget(self.imageLabel)
        vbox.addWidget(self.descriptionLabel)

        self.setLayout(vbox)
        '''
        This section sets the title of the winder and organises the user interface elements vertically using the QVBoxLayout
        available through the use of PyQt5. The widgets are arranged in an approachable layout, intuitive to the use of the 
        program.

        '''
        ##################################################################################################################

        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.locationLabel.setAlignment(Qt.AlignCenter)
        self.locationInput.setAlignment(Qt.AlignCenter)
        self.fullLocationLabel.setAlignment(Qt.AlignCenter)
        self.temperatureLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        
        self.titleLabel.setObjectName("titleLabel")
        self.locationLabel.setObjectName("locationLabel")
        self.locationInput.setObjectName("locationInput")
        self.getWeatherButton.setObjectName("getWeatherButton")
        self.fullLocationLabel.setObjectName("fullLocationLabel")
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.imageLabel.setObjectName("imageLabel")
        self.descriptionLabel.setObjectName("descriptionLabel")

        ################################################# DESIGN OF GUI #################################################
        
        self.setStyleSheet("""
            QWidget{
                background-color: lightblue;            
            } 
            QLabel, QPushButton{
                font-family: Algerian;
            }              
            QLabel#titleLabel{
                font-size: 75px;
                font-weight: bold;
            }
            QLabel#locationLabel{
                font-size: 30px;
                font-style: bold;
            }
            QLineEdit#locationInput{
                font-size: 30px;
            }
            QPushButton#getWeatherButton{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#fullLocationLabel{
                font-size: 30px            
            }
            QLabel#temperatureLabel{
                font-size: 30px;
            }
            QLabel#imageLabel{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#descriptionLabel{
                font-size: 50px;
            }
        """)
        
        ##################################################################################################################

        self.getWeatherButton.clicked.connect(self.getWeather)

    def getWeather(self):
        api_key="58eeba10a44d0dc38ddd64adb50fb76f"
        city = self.locationInput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        ##################################################################################################################
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"]==200:
                self.displayWeather(data)

        ##################################################################################################################
                
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.displayError("Bad request \nPlease check your intput")
                case 401:
                    self.displayError("Unauthorised \nInvalid API Key")
                case 403:
                    self.displayError("Forbidden\nAccess Denied")
                case 404:
                    self.displayError("Not Found\nCity Invalid")
                case 500:
                    self.displayError("Internal Server Error\nTry Again Later")
                case 502:
                    self.displayError("Bad Gateway\n Invalid response from server")
                case 503:
                    self.displayError("Service Unavailable\nServer is down")
                case 504:
                    self.displayError("Gateway Timeout\n No Response from the server")
                case _:
                    self.displayError(f"HTTP Error Occured\n{http_error}")  

        ##################################################################################################################  
        
        except requests.exceptions.ConnectionError:
            self.displayError("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.displayError("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.displayError("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.displayError(f"HTTP error occured\n{req_error}")
        
        ##################################################################################################################

    def displayError(self, message):
        self.fullLocationLabel.setText(" ")
        self.temperatureLabel.setText(message)

        ##################################################################################################################


    def displayWeather(self, data):
        print(data)
        temperatureKelvin = data["main"]["temp"]
        fullLocation = data["sys"]["country"]
        temperatureCelcius = temperatureKelvin-273.15
        self.temperatureLabel.setText(f"{temperatureCelcius}C")
        self.fullLocationLabel.setText(f"{fullLocation}")

        ##################################################################################################################

if __name__=="__main__":
    app = QApplication(sys.argv)
    weather_app=WeatherWatcher()
    weather_app.show()
    sys.exit(app.exec_())
    