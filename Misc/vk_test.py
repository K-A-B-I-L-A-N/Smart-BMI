import glob
import os
import sys
import numpy as np
import time

import serial
import serial.tools.list_ports
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *        

class VKWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\English\VirtualKeyboardWindow.ui",self)
        self.move(640,612)
        self.lower_flag = 1
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)

        self.names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.','-',':','@',
                 '+']
        self.buttons = [self.a_bt,self.b_bt,self.c_bt,self.d_bt,self.e_bt,self.f_bt,self.g_bt,self.h_bt,
                        self.i_bt,self.j_bt,self.k_bt,self.l_bt,self.m_bt,self.n_bt,self.o_bt,self.p_bt,
                        self.q_bt,self.r_bt,self.s_bt,self.t_bt,self.u_bt,self.v_bt,self.w_bt,self.x_bt,
                        self.y_bt,self.z_bt,self.one_bt,self.two_bt,self.three_bt,self.four_bt,self.five_bt,
                        self.six_bt,self.seven_bt,self.eight_bt,self.nine_bt,self.zero_bt,self.dot_bt,
                        self.hyphen_bt,self.colon_bt,self.at_bt,self.plus_bt]
        ##clicked functions
        
        for button,name in zip(self.buttons,self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button,button.KEY_CHAR)


        self.clr_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.clr_bt,Qt.Key_Clear)

        self.caps_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.caps_bt,Qt.Key_CapsLock)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt,Qt.Key_Backspace)

        self.spc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.spc_bt,Qt.Key_Space)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt,Qt.Key_Home)

        self.kbip.setFocus()

    def buttonClicked(self,char_ord):
        txt = self.kbip.text()

        if char_ord == Qt.Key_Clear:
            txt = ''

        elif char_ord == Qt.Key_CapsLock:

            if self.lower_flag == 0:
                self.lower_flag = 1

            else:
                self.lower_flag = 0


        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1] 

        elif char_ord == Qt.Key_Space:
            txt += ' ' 

        elif char_ord == Qt.Key_Home:
            #not done
            pass

        else:
            try:
                if self.lower_flag == 1:
                    txt += chr(char_ord).lower()
                else:
                    txt += chr(char_ord)
            except:
                pass

        self.kbip.setText(txt)
        self.kbip.setFocus()


app = QApplication(sys.argv)
ui = VKWindow()
ui.show()
app.exec_()
