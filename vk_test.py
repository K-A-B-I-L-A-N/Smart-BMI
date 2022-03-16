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


class KBIPWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\KeyboardInputWindow.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(640,300)
        self.clr_bt.clicked.connect(self.clear_text)
        self.clr_bt.setVisible(False)
        self.kbip.textChanged.connect(self.show_clr_bt)

    def clear_text(self):
        self.kbip.clear()

    def show_clr_bt(self):

        self.kbip.setFocus()
        if len(self.kbip.text()) == 0:
            self.clr_bt.setVisible(False)
        else:
            self.clr_bt.setVisible(True)

class AlphabetsWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\AlphabetWindow.ui", self)
        self.lower_flag = 1
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)
        self.names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.buttons = [self.a_bt, self.b_bt, self.c_bt, self.d_bt, self.e_bt, self.f_bt, self.g_bt, self.h_bt,
                        self.i_bt, self.j_bt, self.k_bt, self.l_bt, self.m_bt, self.n_bt, self.o_bt, self.p_bt,
                        self.q_bt, self.r_bt, self.s_bt, self.t_bt, self.u_bt, self.v_bt, self.w_bt, self.x_bt,
                        self.y_bt, self.z_bt]
        # clicked functions

        for button, name in zip(self.buttons, self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button, button.KEY_CHAR)

        self.caps_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.caps_bt, Qt.Key_CapsLock)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt, Qt.Key_Backspace)

        self.spc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.spc_bt, Qt.Key_Space)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt, Qt.Key_Home)

        self.ns_bt.clicked.connect(self.show_nsw)

    def show_nsw(self):
        widget.setCurrentWidget(nsW)
        # to create an object for nswindow and show here


    def buttonClicked(self, char_ord):
        txt = kbipW.kbip.text()

        if char_ord == Qt.Key_CapsLock:

            if self.lower_flag == 0:
                self.lower_flag = 1
                self.caps_bt.setIcon(QIcon(QPixmap("designs\icons\caps off.png")))
                for button in self.buttons:
                    button.setText(button.text().lower())

            else:
                self.lower_flag = 0
                self.caps_bt.setIcon(QIcon(QPixmap("designs\icons\caps on.png")))
                for button in self.buttons:
                    button.setText(button.text().upper())


        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            pass
            widget.close()
            kbipW.close()
            # self.LE.setText(txt)

        else:
            try:
                if self.lower_flag == 1:
                    txt += chr(char_ord).lower()
                else:
                    txt += chr(char_ord)
            except:
                pass

        kbipW.activateWindow()
        kbipW.kbip.setText(txt)
        kbipW.kbip.setFocus()

    # def kb_disp(self, event):

    #     if ui.mmW.Password_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.mmW.Password_ip.text())
    #         self.show()
    #         self.LE = ui.mmW.Password_ip

    #     elif ui.smscW.Msg_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.smscW.Msg_ip.toPlainText())
    #         self.show()
    #         self.LE = ui.smscW.Msg_ip

    #     elif ui.pssW.Hd1_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd1_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd1_ip

    #     elif ui.pssW.Hd2_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd2_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd2_ip

    #     elif ui.pssW.Hd3_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd3_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd3_ip

    #     elif ui.pssW.Ft1_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft1_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft1_ip

    #     elif ui.pssW.Ft2_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft2_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft2_ip

    #     elif ui.pssW.Ft3_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft3_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft3_ip

###################################################################################

class NumpadWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NumpadWindow.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)

        self.names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', '/', '-', '*']
        self.buttons = [self.one_bt, self.two_bt, self.three_bt, self.four_bt, self.five_bt,
                        self.six_bt, self.seven_bt, self.eight_bt, self.nine_bt, self.zero_bt,
                        self.dot_bt, self.comma_bt, self.fslash_bt, self.hyphen_bt, self.star_bt]

        # clicked functions
        for button, name in zip(self.buttons, self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button, button.KEY_CHAR)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt, Qt.Key_Backspace)

        self.spc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.spc_bt, Qt.Key_Space)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt, Qt.Key_Home)

    def buttonClicked(self, char_ord):
        txt = kbipW.kbip.text()

        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            widget.close()
            kbipW.close()
            # self.LE.setText(txt)

        else:
            txt += chr(char_ord)
            # try:
            #     if self.lower_flag == 1:
            #         txt += chr(char_ord).lower()
            #     else:
            #         txt += chr(char_ord)
            # except:
            #     pass

        kbipW.kbip.setText(txt)
        kbipW.activateWindow()
        kbipW.kbip.setFocus()

    # def kb_disp(self, event):

    #     if ui.wcW.Mc_ip.hasFocus():
    #         self.hide()
    #         self.kpip.setText(ui.wcW.Mc_ip.text())
    #         self.kpip.setMaxLength(32767)
    #         self.show()
    #         self.LE = ui.wcW.Mc_ip

    #     elif ui.wcW.Cc_ip.hasFocus():
    #         self.hide()
    #         self.kpip.setText(ui.wcW.Cc_ip.text())
    #         self.kpip.setMaxLength(32767)
    #         self.show()
    #         self.LE = ui.wcW.Cc_ip

    #     elif ui.hcW.RefH_ip.hasFocus():
    #         self.hide()
    #         self.kpip.setText(ui.hcW.RefH_ip.text())
    #         self.kpip.setMaxLength(32767)
    #         self.show()
    #         self.LE = ui.hcW.RefH_ip

    #     elif ui.smscW.Mbno_ip.hasFocus():
    #         self.hide()
    #         self.kpip.setText(ui.smscW.Mbno_ip.text())
    #         self.kpip.setMaxLength(10)
    #         self.show()
    #         self.LE = ui.smscW.Mbno_ip

    #     elif ui.ssmsW.Mbno_ip.hasFocus():
    #         self.hide()
    #         self.kpip.setText(ui.ssmsW.Mbno_ip.text())
    #         self.kpip.setMaxLength(10)
    #         self.show()
    #         self.LE = ui.ssmsW.Mbno_ip

#############################################################################################

class NumbersandSymbolsWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NumberandSymbolsWindow.ui", self)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.move(640, 375)
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)
        self.names = ['1','2','3','4','5','6','7','8','9','0','-','/',
                      ':','~','(',')','$','&',"'",'"','+','@','.',',',
                      '?','!','#','%','*']

        self.buttons = [self.one_bt, self.two_bt, self.three_bt, self.four_bt, self.five_bt, self.six_bt, self.seven_bt, self.eight_bt,
                        self.nine_bt, self.zero_bt, self.hyphen_bt, self.fslash_bt, self.colon_bt, self.tilde_bt, self.ob_bt, self.cb_bt,
                        self.dollar_bt, self.and_bt, self.sapostrophe_bt, self.dapostrophe_bt, self.plus_bt, self.at_bt, self.dot_bt, 
                        self.comma_bt, self.qmark_bt, self.excmark_bt, self.hash_bt, self.percentage_bt,self.star_bt]
        # clicked functions

        for button, name in zip(self.buttons, self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button, button.KEY_CHAR)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt, Qt.Key_Backspace)

        self.spc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.spc_bt, Qt.Key_Space)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt, Qt.Key_Home)

        self.abc_bt.clicked.connect(self.show_abc)

    def show_abc(self):
        widget.setCurrentWidget(alpW)


    def buttonClicked(self, char_ord):
        txt = kbipW.kbip.text()

        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            widget.close()
            kbipW.close()
            # self.LE.setText(txt)

        else:
            txt += chr(char_ord)
            # try:
            #     if self.lower_flag == 1:
            #         txt += chr(char_ord).lower()
            #     else:
            #         txt += chr(char_ord)
            # except:
            #     pass

        kbipW.activateWindow()
        kbipW.kbip.setText(txt)
        kbipW.kbip.setFocus()

    # def kb_disp(self, event):

    #     if ui.mmW.Password_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.mmW.Password_ip.text())
    #         self.show()
    #         self.LE = ui.mmW.Password_ip

    #     elif ui.smscW.Msg_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.smscW.Msg_ip.toPlainText())
    #         self.show()
    #         self.LE = ui.smscW.Msg_ip

    #     elif ui.pssW.Hd1_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd1_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd1_ip

    #     elif ui.pssW.Hd2_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd2_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd2_ip

    #     elif ui.pssW.Hd3_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Hd3_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Hd3_ip

    #     elif ui.pssW.Ft1_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft1_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft1_ip

    #     elif ui.pssW.Ft2_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft2_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft2_ip

    #     elif ui.pssW.Ft3_ip.hasFocus():
    #         self.hide()
    #         self.kbip.setText(ui.pssW.Ft3_ip.text())
    #         self.show()
    #         self.LE = ui.pssW.Ft3_ip



#############################################################################################



app = QApplication(sys.argv)
widget = QStackedWidget()
widget.setStyleSheet("QStackedWidget{background-color: rgb(35, 35, 35);border-radius:15px;}")
widget.setGeometry(640, 375, 600, 375)
widget.setWindowFlag(Qt.FramelessWindowHint)
kbipW = KBIPWindow()
alpW = AlphabetsWindow()
nsW = NumbersandSymbolsWindow()
npW = NumpadWindow()
widget.addWidget(alpW)
widget.addWidget(nsW)
widget.addWidget(npW)
widget.setCurrentWidget(npW)
kbipW.show()
widget.show()
app.exec_()
