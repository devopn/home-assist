# http://146.0.79.198:5000/get_state

import sys
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import datetime
from PyQt5.QtCore import QTimer
from server import Server
from PlotterWindow import PlotterWindow

class SmartHomeWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)
        # INIT SERVER
        self.server = Server("146.0.79.198", "5000")

        # Connect color sliders to button
        self.slider_blue.valueChanged.connect(self.change_button_color)
        self.slider_green.valueChanged.connect(self.change_button_color)
        self.slider_red.valueChanged.connect(self.change_button_color)
        actual_data = self.get_data_from_server()
        if actual_data != -1:
            self.slider_red.setValue(int(actual_data["color"][0:2], 16))
            self.slider_green.setValue(int(actual_data["color"][2:4], 16))
            self.slider_blue.setValue(int(actual_data["color"][4:6], 16))
            self.temperature_value.setText(str(actual_data["temp"]) + "\u00b0C")
            self.humidity_value.setText(str(actual_data["hum"]) + "%")

        # Set colors to server
        self.button_color_update.clicked.connect(self.set_color_to_server)

        # Create timer to update data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.setInterval(self.freq_spin.value() * 1000)
        self.timer.start()
        self.freq_spin.valueChanged.connect(self.timer_setInterval)

        # Create timer to clock
        self.update_clock()
        self.clock = QTimer()
        self.clock.timeout.connect(self.update_clock)
        self.clock.start(1000)
        self.clock.start()

        # Connect graph buttons
        self.button_humidity_graph.clicked.connect(self.plote_hum)
        self.button_temperature_graph.clicked.connect(self.plote_temp)
        

    def change_button_color(self):
        r = self.slider_red.value()
        g = self.slider_green.value()
        b = self.slider_blue.value()
        style = "background-color: #{:02X}{:02X}{:02X};".format(r, g, b)
        style += "color: #{:02X}{:02X}{:02X}".format(
            255 - r, 255 - g, 255 - b
        )  # Set contrast color of text
        self.button_color_update.setStyleSheet(style)

    def get_data_from_server(self):
        data = self.server.get_data()
        if data == -1:
            self.statusbar.showMessage(
                "Error getting data from server"
            )
        else:
            return data

    def set_data_to_server(self, data):
        response_code = self.server.set_data(data)
        if response_code == 200:
            self.statusbar.showMessage("Success")
        else:
            self.statusbar.showMessage(
                "Error sending data to server #{}".format(response_code)
            )

    def set_color_to_server(self):
        r = self.slider_red.value()
        g = self.slider_green.value()
        b = self.slider_blue.value()
        color = "{:02X}{:02X}{:02X}".format(r, g, b)
        data = self.get_data_from_server()
        if data != -1:
            data["color"] = color
            self.set_data_to_server(json.dumps(data))

    def timer_setInterval(self):
        self.timer.setInterval(self.freq_spin.value() * 1000)

    def update_data(self):
        data = self.get_data_from_server()
        if data != -1:
            self.temperature_value.setText(str(round(data["temp"],1)) + "\u00b0C")
            self.humidity_value.setText(str(round(data["hum"], 1)) + "%")
            print

    def update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.setText(now.strftime("%H:%M:%S"))
        
    def plote_temp(self):
        num = 1000
        data = self.server.get_history(num)
        dataY = [data.get(str(i))[1] for i in range(num) if i % 4 ==0]
        dataX = [":".join(data.get(str(i))[0].split(" ")[1].split(":")[:2]) for i in range(num) if i % 4 ==0]
        print(data)
        # print(dataX)
        self.win = PlotterWindow(dataX[::-1], dataY[::-1])
        self.win.show()

    def plote_hum(self):
        num = 1000
        data = self.server.get_history(num)
        dataY = [data.get(str(i))[2] for i in range(num) if i % 4 ==0]
        dataX = [":".join(data.get(str(i))[0].split(" ")[1].split(":")[:2]) for i in range(num) if i % 4 ==0]
        # print(dataX)
        self.win = PlotterWindow(dataX[::-1], dataY[::-1])
        self.win.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SmartHomeWidget()
    ex.show()
    sys.exit(app.exec_())



