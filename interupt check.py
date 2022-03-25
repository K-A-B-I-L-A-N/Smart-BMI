from ui import Ui_MainWindow
from PyQt5.QtCore import *
from subprocess import check_output
import time
import sys
from PyQt5.QtWidgets import *


class Interupt(QThread):
    def __init__(self):
        super(Interupt, self).__init__()
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        self.current = 0
        self.prev = 0
        self.count = 0

    def run(self):
        while True:
            # self.current = check_output("cat /dev/chipsee-gpio7", shell=True)
            # self.current = self.current[0]-48
            self.current = 1
            if self.current == 1 and self.prev == 0:
                self.count += 1
                self.ui.label.setText(str(self.count))
            self.prev = self.current
            time.sleep(0.05)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    thread = Interupt()
    thread.start()
    sys.exit(app.exec_())