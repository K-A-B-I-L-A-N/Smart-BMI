import glob
import os
import sys
import time
import serial
import threading
import serial.tools.list_ports
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *


# APP
#####################################################################################

class ImageAdDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advertisement")
        self.resize(600, 1024)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("Saved videos\Img_SS.avi")))
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.checker)

    def checker(self, state):
        if state == 0:
            self.mediaPlayer.play()

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.mediaPlayer.stop()
            if gv.SettingsInputs.value('Language') == 'English':
                ui.setandplay_bgm(insertcoin)
            else:
                ui.setandplay_bgm(insertcoin_tamil)
            ui.widget.setCurrentWidget(ui.InsertW)


######################################################################################

class VideoAdDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advertisement")
        self.resize(600, 1024)
        #######
        self.index = 0
        self.flag = 0
        self.clips = glob.glob(R'Videos\*.avi')
        self.filename = self.clips[0]
        #######
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.checker)

    def checker(self, state):
        if state == 0:
            self.next_on_track()

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.flag = 1
            self.index = 0
            self.filename = self.clips[0]
            self.mediaPlayer.stop()
            self.flag = 0
            if gv.SettingsInputs.value('Language') == 'English':
                ui.setandplay_bgm(insertcoin)
            else:
                ui.setandplay_bgm(insertcoin_tamil)
            ui.widget.setCurrentWidget(ui.InsertW)

    def video_run(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.filename)))
        self.mediaPlayer.play()

    def next_on_track(self):
        if self.flag == 0:
            if self.index != len(self.clips):
                try:
                    self.index += 1
                    self.filename = self.clips[self.index]
                except:
                    self.index = 0
                    self.filename = self.clips[self.index]
                self.video_run()

############################################################################


class InsertWindow(QMainWindow):
    def __init__(self):
        # load ui
        super().__init__()
        uic.loadUi("UI Files\InsertWindow.ui", self)

    def keyPressEvent(self, event):

        if event.key() == 65:
            reply = QMessageBox.question(None, "Wish", "Do you want to display weight?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                ui.setandplay_bgm(background)
                ui.widget.setCurrentWidget(ui.bmiW)
                ui.bmiW.countdown()
            
            if reply == QMessageBox.No:
                ui.setandplay_bgm(background)
                ui.widget.setCurrentWidget(ui.bmiwwdW)
                ui.bmiwwdW.countdown()

        if event.key() == 83:
            ui.mmW.setFocus()
            ui.setandplay_bgm(background)
            ui.widget.setCurrentWidget(ui.mmW)

#############################################################################


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\MainMenuWindow.ui", self)
        self.Admin_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Admin_bt.clicked.connect(self.enterpassword)
        self.Login_bt.clicked.connect(self.gotoSettingsOptions)
        self.Cancel_bt.clicked.connect(self.cancel)
        self.Back_bt.clicked.connect(self.gotoAD)
        self.Password_ip.mousePressEvent = KB.alpW.kb_disp

    def keyPressEvent(self, event):
        if event.key() == 65:
            self.Admin_bt.setVisible(True)

    def enterpassword(self):
        self.Password_label.setVisible(True)
        self.Password_ip.setVisible(True)
        self.Login_bt.setVisible(True)
        self.Cancel_bt.setVisible(True)

    def cancel(self):
        self.Password_ip.clear()
        self.Admin_bt.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)

    def gotoSettingsOptions(self):

        if self.Password_ip.text() == 'admin':
            self.Password_ip.clear()
            self.Admin_bt.setVisible(False)
            self.Login_bt.setVisible(False)
            self.Cancel_bt.setVisible(False)
            self.Password_label.setVisible(False)
            self.Password_ip.setVisible(False)
            ui.widget.setCurrentWidget(ui.OptionsW)

        else:
            self.Password_ip.clear()
            msg = QMessageBox()
            msg.setText("Enter the correct password")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    def gotoAD(self):
        self.Admin_bt.setVisible(False)
        self.Password_ip.clear()
        self.Admin_bt.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)
        ui.stop_bgm()
        ui.run_ad()

####################################################################################


class SettingsOptions(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\SettingsOptions.ui", self)
        self.Lang_cb.setCurrentText(gv.SettingsInputs.value('Language'))
        self.Ad_cb.setCurrentText(gv.SettingsInputs.value('Screensaver'))
        self.Signout_bt.clicked.connect(self.gotoAD)
        self.Setup_bt.clicked.connect(self.gotoSetupWindow)
        self.Ad_cb.currentTextChanged.connect(self.setAd)
        self.Lang_cb.currentTextChanged.connect(self.setLang)
        self.Weightcal_bt.clicked.connect(self.gotoWCWindow)
        self.Heightcal_bt.clicked.connect(self.gotoHCWindow)
        self.Sms_bt.clicked.connect(self.gotoSMSCWindow)
        self.Report_bt.clicked.connect(self.gotoRWindow)
        self.Diagnostic_bt.clicked.connect(self.gotoDiagWindow)
        self.Printsetup_bt.clicked.connect(self.gotoPSSWindow)

    def setAd(self, state):
        if state == 'Videos':
            gv.SettingsInputs.setValue('Screensaver', 'Videos')
        else:
            gv.SettingsInputs.setValue('Screensaver', 'Images')

    def setLang(self, state):
        if state == 'Tamil':
            gv.SettingsInputs.setValue('Language', 'Tamil')
        else:
            gv.SettingsInputs.setValue('Language', 'English')

    def gotoAD(self):
        ui.stop_bgm()
        ui.run_ad()

    def gotoWCWindow(self):
        ui.widget.setCurrentWidget(ui.wcW)

    def gotoHCWindow(self):
        ui.widget.setCurrentWidget(ui.hcW)

    def gotoSMSCWindow(self):
        ui.widget.setCurrentWidget(ui.smscW)

    def gotoRWindow(self):
        ui.widget.setCurrentWidget(ui.rW)

    def gotoDiagWindow(self):
        ui.widget.setCurrentWidget(ui.dW)

    def gotoPSSWindow(self):
        ui.widget.setCurrentWidget(ui.pssW)

    def gotoSetupWindow(self):
        ui.widget.setCurrentWidget(ui.setupW)


########################################################################################

class SetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\SetupWindow.ui", self)
        self.Pos_cb.setCurrentText(gv.SettingsInputs.value('Print or SMS'))
        self.Wd_cb.setCurrentText(gv.SettingsInputs.value('Weight Display'))
        self.Back_bt.clicked.connect(self.gotoSettingsOptions_Back)
        self.Save_bt.clicked.connect(self.gotoSettingsOptions_Save)

    def gotoSettingsOptions_Back(self):
        ui.widget.setCurrentWidget(ui.OptionsW)

    def gotoSettingsOptions_Save(self):

        if self.Pos_cb.currentText() == 'Print only':
            gv.SettingsInputs.setValue('Print or SMS', 'Print only')
        else:
            gv.SettingsInputs.setValue("Print or SMS", 'Print and SMS')

        if self.Wd_cb.currentText() == 'Yes':
            gv.SettingsInputs.setValue('Weight Display', 'Yes')
        else:
            gv.SettingsInputs.setValue('Weight Display', 'No')

        self.gotoSettingsOptions_Back()

#######################################################################################


class WCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\WeightCalibrationWindow.ui", self)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)
        self.Mc_ip.mousePressEvent = KB.npW.kb_disp
        self.Cc_ip.mousePressEvent = KB.npW.kb_disp

    def gotoSettingsOptions(self):
        ui.widget.setCurrentWidget(ui.OptionsW)


########################################################################################


class HCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\HeightCalibrationWindow.ui", self)
        self.Signout_bt.clicked.connect(self.gotoSettingsOptions)
        self.Ah_lb.setVisible(False)
        self.Ah_val.setVisible(False)
        self.Adc_lb.setVisible(False)
        self.Adc_val.setVisible(False)
        self.RefH_lb.setVisible(False)
        self.RefH_ip.setVisible(False)
        self.Close_bt.clicked.connect(self.hide)
        self.Set_bt.clicked.connect(self.show_params)
        self.RefH_ip.mousePressEvent = KB.npW.kb_disp

    def show_params(self):
        self.Ah_lb.setVisible(True)
        self.Ah_val.setVisible(True)
        self.Adc_lb.setVisible(True)
        self.Adc_val.setVisible(True)
        self.RefH_lb.setVisible(True)
        self.RefH_ip.setVisible(True)

    def hide(self):
        self.Ah_lb.setVisible(False)
        self.Ah_val.setVisible(False)
        self.Adc_lb.setVisible(False)
        self.Adc_val.setVisible(False)
        self.RefH_lb.setVisible(False)
        self.RefH_ip.setVisible(False)

    def gotoSettingsOptions(self):
        self.hide()
        ui.widget.setCurrentWidget(ui.OptionsW)


############################################################################


class SMSCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\SMSConfigWindow.ui", self)
        self.Dc_bt.setEnabled(False)
        self.Send_bt.setEnabled(False)
        self.C_bt.clicked.connect(self.enable)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)
        self.Mbno_ip.setText(gv.SettingsInputs.value('smscW Mbno'))
        self.Msg_ip.setText(gv.SettingsInputs.value('smscW Msg'))
        self.Mbno_ip.mousePressEvent = KB.npW.kb_disp
        self.Msg_ip.mousePressEvent = KB.alpW.kb_disp

    def enable(self):
        self.Dc_bt.setEnabled(True)
        self.Send_bt.setEnabled(True)

    def gotoSettingsOptions(self):
        gv.SettingsInputs.setValue('smscW Mbno', self.Mbno_ip.text())
        gv.SettingsInputs.setValue('smscW Msg', self.Msg_ip.toPlainText())
        self.Dc_bt.setEnabled(False)
        self.Send_bt.setEnabled(False)
        ui.widget.setCurrentWidget(ui.OptionsW)


##############################################################################


class RWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\ReportWindow.ui", self)
        self.Ok_bt.clicked.connect(self.gotoSettingsOptions)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentWidget(ui.OptionsW)


###############################################################################


class DiagWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\DiagnosticsWindow.ui", self)
        self.Close_bt.clicked.connect(self.gotoSettingsOptions)
        # O/P on buttons
        # self.op1_onbt.clicked.connect(self.on_op)
        self.op1_onbt.clicked.connect(lambda flag, i=1: self.on_op(flag, i))
        self.op2_onbt.clicked.connect(lambda flag, i=2: self.on_op(flag, i))
        self.op3_onbt.clicked.connect(lambda flag, i=3: self.on_op(flag, i))
        self.op4_onbt.clicked.connect(lambda flag, i=4: self.on_op(flag, i))
        self.op5_onbt.clicked.connect(lambda flag, i=5: self.on_op(flag, i))
        self.op6_onbt.clicked.connect(lambda flag, i=6: self.on_op(flag, i))
        self.op7_onbt.clicked.connect(lambda flag, i=7: self.on_op(flag, i))
        self.op8_onbt.clicked.connect(lambda flag, i=8: self.on_op(flag, i))
        # O/P off buttons
        self.op1_offbt.clicked.connect(lambda flag, i=1: self.off_op(flag, i))
        self.op2_offbt.clicked.connect(lambda flag, i=2: self.off_op(flag, i))
        self.op3_offbt.clicked.connect(lambda flag, i=3: self.off_op(flag, i))
        self.op4_offbt.clicked.connect(lambda flag, i=4: self.off_op(flag, i))
        self.op5_offbt.clicked.connect(lambda flag, i=5: self.off_op(flag, i))
        self.op6_offbt.clicked.connect(lambda flag, i=6: self.off_op(flag, i))
        self.op7_offbt.clicked.connect(lambda flag, i=7: self.off_op(flag, i))
        self.op8_offbt.clicked.connect(lambda flag, i=8: self.off_op(flag, i))

    def on_op(self, flag, i):
        if i == 1:
            self.op1_lb.setStyleSheet("background-color:green")
        if i == 2:
            self.op2_lb.setStyleSheet("background-color:green")
        if i == 3:
            self.op3_lb.setStyleSheet("background-color:green")
        if i == 4:
            self.op4_lb.setStyleSheet("background-color:green")
        if i == 5:
            self.op5_lb.setStyleSheet("background-color:green")
        if i == 6:
            self.op6_lb.setStyleSheet("background-color:green")
        if i == 7:
            self.op7_lb.setStyleSheet("background-color:green")
        if i == 8:
            self.op8_lb.setStyleSheet("background-color:green")

    def off_op(self, flag, i):
        if i == 1:
            self.op1_lb.setStyleSheet("background-color:red")
        if i == 2:
            self.op2_lb.setStyleSheet("background-color:red")
        if i == 3:
            self.op3_lb.setStyleSheet("background-color:red")
        if i == 4:
            self.op4_lb.setStyleSheet("background-color:red")
        if i == 5:
            self.op5_lb.setStyleSheet("background-color:red")
        if i == 6:
            self.op6_lb.setStyleSheet("background-color:red")
        if i == 7:
            self.op7_lb.setStyleSheet("background-color:red")
        if i == 8:
            self.op8_lb.setStyleSheet("background-color:red")

    def gotoSettingsOptions(self):
        ui.widget.setCurrentWidget(ui.OptionsW)


###############################################################################

class PSSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\PrintSlipSettingsWindow.ui", self)
        self.list = []
        self.Save_bt.clicked.connect(self.saveOptions)
        self.Cancel_bt.clicked.connect(self.gotoSettingsOptions)
        self.H_def_rb.clicked.connect(self.showdef_Hvalues)
        self.H_text_rb.clicked.connect(self.showsaved_Hvalues)
        self.F_def_rb.clicked.connect(self.showdef_Fvalues)
        self.F_text_rb.clicked.connect(self.showsaved_Fvalues)
        self.Yes_rb.clicked.connect(self.show_footer)
        self.No_rb.clicked.connect(self.hide_footer)
        self.Hd1_ip.mousePressEvent = KB.alpW.kb_disp
        self.Hd2_ip.mousePressEvent = KB.alpW.kb_disp
        self.Hd3_ip.mousePressEvent = KB.alpW.kb_disp
        self.Ft1_ip.mousePressEvent = KB.alpW.kb_disp
        self.Ft2_ip.mousePressEvent = KB.alpW.kb_disp
        self.Ft3_ip.mousePressEvent = KB.alpW.kb_disp
        self.setOptions()

    def setOptions(self):

        for i in gv.SettingsInputs.value("PSS"):
            if i == 'true':
                self.list.append(True)
            elif i == 'false':
                self.list.append(False)
            else:
                self.list.append(i)

        if self.list[0] == 'Default':
            self.H_def_rb.setChecked(True)
            self.showdef_Hvalues()
        else:
            self.H_text_rb.setChecked(True)
            self.showsaved_Hvalues()

        if self.list[1] == 'Default':
            self.F_def_rb.setChecked(True)
            self.showdef_Fvalues()
        else:
            self.F_text_rb.setChecked(True)
            self.showsaved_Fvalues()

        if self.list[2] == 'Yes':
            self.Yes_rb.setChecked(True)
        else:
            self.No_rb.setChecked(True)
            self.hide_footer()

        self.Hd1_cb.setChecked(self.list[3])
        self.Hd2_cb.setChecked(self.list[4])
        self.Hd3_cb.setChecked(self.list[5])
        self.Ft1_cb.setChecked(self.list[6])
        self.Ft2_cb.setChecked(self.list[7])
        self.Ft3_cb.setChecked(self.list[8])

    def hide_footer(self):
        self.Ft1_lb.setVisible(False)
        self.Ft2_lb.setVisible(False)
        self.Ft3_lb.setVisible(False)
        self.Ft1_ip.setVisible(False)
        self.Ft2_ip.setVisible(False)
        self.Ft3_ip.setVisible(False)
        self.Ft1_cb.setVisible(False)
        self.Ft2_cb.setVisible(False)
        self.Ft3_cb.setVisible(False)

    def show_footer(self):
        self.Ft1_lb.setVisible(True)
        self.Ft2_lb.setVisible(True)
        self.Ft3_lb.setVisible(True)
        self.Ft1_ip.setVisible(True)
        self.Ft2_ip.setVisible(True)
        self.Ft3_ip.setVisible(True)
        self.Ft1_cb.setVisible(True)
        self.Ft2_cb.setVisible(True)
        self.Ft3_cb.setVisible(True)

    def saveOptions(self):
        if self.H_def_rb.isChecked():
            self.list[0] = 'Default'
        else:
            self.list[0] = 'Text'
            gv.SettingsInputs.setValue('Header 1', self.Hd1_ip.text())
            gv.SettingsInputs.setValue('Header 2', self.Hd2_ip.text())
            gv.SettingsInputs.setValue('Header 3', self.Hd3_ip.text())

        if self.F_def_rb.isChecked():
            self.list[1] = 'Default'
        else:
            self.list[1] = 'Text'
            gv.SettingsInputs.setValue('Footer 1', self.Ft1_ip.text())
            gv.SettingsInputs.setValue('Footer 2', self.Ft2_ip.text())
            gv.SettingsInputs.setValue('Footer 3', self.Ft3_ip.text())

        if self.Yes_rb.isChecked():
            self.list[2] = 'Yes'
        else:
            self.list[2] = 'No'

        self.list[3:9] = [self.Hd1_cb.isChecked(), self.Hd2_cb.isChecked(), self.Hd3_cb.isChecked(),
                          self.Ft1_cb.isChecked(), self.Ft2_cb.isChecked(), self.Ft3_cb.isChecked()]

        gv.SettingsInputs.setValue('PSS', self.list)

        if (len(self.Hd1_ip.text()) > 0 and len(self.Hd2_ip.text()) > 0 and len(self.Hd3_ip.text()) > 0
                and len(self.Ft1_ip.text()) > 0 and len(self.Ft2_ip.text()) > 0 and len(self.Ft3_ip.text()) > 0):

            self.gotoSettingsOptions()

        else:

            msg = QMessageBox()
            msg.setText("Don't Leave Textfields empty")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    def gotoSettingsOptions(self):
        ui.widget.setCurrentWidget(ui.OptionsW)

    def showdef_Hvalues(self):
        self.Hd1_ip.setText("SMART BMI SYSTEM")
        self.Hd2_ip.setText("SMART BMI -A7")
        self.Hd3_ip.setText("Chennai")
        self.Hd1_ip.setEnabled(False)
        self.Hd2_ip.setEnabled(False)
        self.Hd3_ip.setEnabled(False)

    def showdef_Fvalues(self):
        self.Ft1_ip.setText("Lcs Controls Pvt Ltd")
        self.Ft2_ip.setText("Contact No: 9444024124")
        self.Ft3_ip.setText("sales@lcscontrol.in")
        self.Ft1_ip.setEnabled(False)
        self.Ft2_ip.setEnabled(False)
        self.Ft3_ip.setEnabled(False)

    def showsaved_Hvalues(self):
        self.Hd1_ip.setText(gv.SettingsInputs.value('Header 1'))
        self.Hd2_ip.setText(gv.SettingsInputs.value('Header 2'))
        self.Hd3_ip.setText(gv.SettingsInputs.value('Header 3'))
        self.Hd1_ip.setEnabled(True)
        self.Hd2_ip.setEnabled(True)
        self.Hd3_ip.setEnabled(True)

    def showsaved_Fvalues(self):
        self.Ft1_ip.setText(gv.SettingsInputs.value('Footer 1'))
        self.Ft2_ip.setText(gv.SettingsInputs.value('Footer 2'))
        self.Ft3_ip.setText(gv.SettingsInputs.value('Footer 3'))
        self.Ft1_ip.setEnabled(True)
        self.Ft2_ip.setEnabled(True)
        self.Ft3_ip.setEnabled(True)


###############################################################################


class BMI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\BMIWindow.ui", self)
        self.needle_1.setHidden(True)
        self.needle_2.setHidden(True)
        self.needle_3.setHidden(True)
        self.needle_4.setHidden(True)
        self.needle_5.setHidden(True)
        self.secs = 10
        self.height.setText(self.get_height())
        self.weight.setText(self.get_weight())
        self.Result.setText(self.get_bmi())

    def get_height(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)

            self.Ht = str(ip.read(13))
            self.Ht = self.Ht[6:13]
            decode = self.Ht.split("-")
            self.Ht = decode[1]
            self.Ht = self.Ht[:len(self.Ht) - int(decode[0])] + \
                "." + self.Ht[len(self.Ht) - int(decode[0]):]
        except:
            self.Ht = "180"
        
        return self.Ht

    def get_weight(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)
            self.Wt = str(ip.read(13))
            self.Wt = self.Wt[6:13]
            decode = self.Wt.split("-")  # [decimal places from right , value]
            self.Wt = decode[1]
            self.Wt = self.Wt[:len(self.Wt) - int(decode[0])] + \
                "." + self.Wt[len(self.Wt) - int(decode[0]):]

        except:
            self.Wt = "75"

        return self.Wt

    def get_bmi(self):
        self.BMIindex = str("{:.2f}".format(
            float(self.Ht) / ((float(self.Wt) / 100) ** 2)))
        
        print(self.BMIindex)

        if self.BMIindex < "20":
            self.needle_1.setHidden(False)
        elif self.BMIindex >= "20" and self.BMIindex < "25":
            self.needle_2.setHidden(False)
        elif self.BMIindex >= "25" and self.BMIindex < "30":
            self.needle_3.setHidden(False)
        elif self.BMIindex >= "30" and self.BMIindex < "35":
            self.needle_4.setHidden(False)
        else:
            self.needle_5.setHidden(False)

        return self.BMIindex

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.lb_timer_bmi.setText("")
            self.secs = 10
            self.timer.stop()
            if gv.SettingsInputs.value('Print or SMS') == 'Print and SMS':
                ui.widget.setCurrentWidget(ui.posW)
                ui.posW.countdown()
            else:
                if gv.SettingsInputs.value('Language') == 'English':
                    ui.setandplay_bgm(printM)
                else:
                    ui.setandplay_bgm(printM_tamil)
                ui.widget.setCurrentWidget(ui.gdapW)
                ui.gdapW.countdown()
        else:
            self.lb_timer_bmi.setText(str(self.secs))
            self.secs -= 1

##################################################################################


class BMIWWD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\BMIWWDWindow.ui", self)
        self.needle_1.setHidden(True)
        self.needle_2.setHidden(True)
        self.needle_3.setHidden(True)
        self.needle_4.setHidden(True)
        self.needle_5.setHidden(True)
        self.secs = 10
        self.height.setText(self.get_height())
        self.get_weight()
        self.Result.setText(self.get_bmi())

    def get_height(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)

            self.Ht = str(ip.read(13))
            self.Ht = self.Ht[6:13]
            decode = self.Ht.split("-")
            self.Ht = decode[1]
            self.Ht = self.Ht[:len(self.Ht) - int(decode[0])] + \
                "." + self.Ht[len(self.Ht) - int(decode[0]):]
        except:
            self.Ht = "180"
        
        return self.Ht

    def get_weight(self):
        # ports = serial.tools.list_ports.comports()
        # print(ports[0])
        try:
            ip = serial.Serial(port="COM6", baudrate=19200, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)
            self.Wt = str(ip.read(13))
            self.Wt = self.Wt[6:13]
            decode = self.Wt.split("-")  # [decimal places from right , value]
            self.Wt = decode[1]
            self.Wt = self.Wt[:len(self.Wt) - int(decode[0])] + \
                "." + self.Wt[len(self.Wt) - int(decode[0]):]

        except:
            self.Wt = "75"

        return self.Wt

    def get_bmi(self):
        self.BMIindex = str("{:.2f}".format(
            float(self.Ht) / ((float(self.Wt) / 100) ** 2)))
        
        print(self.BMIindex)

        if self.BMIindex < "20":
            self.needle_1.setHidden(False)
        elif self.BMIindex >= "20" and self.BMIindex < "25":
            self.needle_2.setHidden(False)
        elif self.BMIindex >= "25" and self.BMIindex < "30":
            self.needle_3.setHidden(False)
        elif self.BMIindex >= "30" and self.BMIindex < "35":
            self.needle_4.setHidden(False)
        else:
            self.needle_5.setHidden(False)

        return self.BMIindex

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.lb_timer_bmi.setText("")
            self.secs = 10
            self.timer.stop()
            if gv.SettingsInputs.value('Print or SMS') == 'Print and SMS':
                ui.widget.setCurrentWidget(ui.posW)
                ui.posW.countdown()
            else:
                if gv.SettingsInputs.value('Language') == 'English':
                    ui.setandplay_bgm(printM)
                else:
                    ui.setandplay_bgm(printM_tamil)
                ui.widget.setCurrentWidget(ui.gdapW)
                ui.gdapW.countdown()
        else:
            self.lb_timer_bmi.setText(str(self.secs))
            self.secs -= 1


##################################################################################

class POSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\PrintorSmsWindow.ui", self)
        self.secs = 10
        self.Print_bt.clicked.connect(self.Print)
        self.Sms_bt.clicked.connect(self.SMS)

    def Print(self):
        self.timer_lb.setText("")
        self.timer.stop()
        self.secs = 10
        if gv.SettingsInputs.value('Language') == 'English':
            ui.setandplay_bgm(printM)
        else:
            ui.setandplay_bgm(printM_tamil)
        ui.widget.setCurrentWidget(ui.gdapW)
        ui.gdapW.countdown()

    def SMS(self):
        self.timer_lb.setText("")
        self.timer.stop()
        self.secs = 10
        ui.widget.setCurrentWidget(ui.ssmsW)

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.timer_lb.setText(str(self.secs))
            self.Print()
        else:
            self.timer_lb.setText(str(self.secs))
            self.secs -= 1


##################################################################################

class SendSMSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\SendSMSWindow.ui", self)
        self.Back_bt.clicked.connect(self.gotoPOSWindow)
        self.Send_bt.clicked.connect(self.gotogdW)
        self.Mbno_ip.mousePressEvent = KB.npW.kb_disp

    def gotoPOSWindow(self):
        self.Mbno_ip.clear()
        ui.posW.countdown()
        ui.widget.setCurrentWidget(ui.posW)

    def gotogdW(self):
        if len(self.Mbno_ip.text()) == 10:
            self.Mbno_ip.clear()
            if gv.SettingsInputs.value('Language') == 'English':
                ui.setandplay_bgm(sms)
            else:
                ui.setandplay_bgm(sms_tamil)
            ui.widget.setCurrentWidget(ui.gdW)
            ui.gdW.countdown()

        else:
            self.Mbno_ip.clear()
            msg = QMessageBox()
            msg.setText("Enter a valid phone number")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


###################################################################################


class GetDownAPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\GetDownAPWindow.ui", self)
        self.secs = 7

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs <= 0:
            self.timer.stop()
            self.secs = 7
            ui.stop_bgm()
            ui.run_ad()
        else:
            self.secs -= 1

###################################################################################


class GetDownWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\GetDownWindow.ui", self)
        self.secs = 7

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs <= 0:
            self.timer.stop()
            self.secs = 7
            ui.stop_bgm()
            ui.run_ad()
        else:
            self.secs -= 1

###################################################################################


class NoPaperWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NoPaperWindow.ui", self)

# APP
###################################################################################


class KBIPWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\KeyboardInputWindow.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(640, 715)
        self.clr_bt.clicked.connect(self.clear_text)
        self.clr_bt.setVisible(False)
        self.kbip.textChanged.connect(self.show_clr_bt)

    def clear_text(self):
        self.kbip.clear()

    def show_clr_bt(self):

        if len(self.kbip.text()) == 0:
            self.clr_bt.setVisible(False)
        else:
            self.clr_bt.setVisible(True)

###################################################################################


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
        KB.kbui.setCurrentWidget(KB.nsW)

    def buttonClicked(self, char_ord):
        # ui.haptic_flag = 1
        txt = KB.kbipW.kbip.text()

        if char_ord == Qt.Key_CapsLock:

            if self.lower_flag == 0:
                self.lower_flag = 1
                self.caps_bt.setIcon(
                    QIcon(QPixmap("designs\icons\caps off.png")))
                for button in self.buttons:
                    button.setText(button.text().lower())

            else:
                self.lower_flag = 0
                self.caps_bt.setIcon(
                    QIcon(QPixmap("designs\icons\caps on.png")))
                for button in self.buttons:
                    button.setText(button.text().upper())

        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            KB.kbui.hide()
            KB.kbipW.hide()
            self.LE.setText(txt)

        else:
            try:
                if self.lower_flag == 1:
                    txt += chr(char_ord).lower()
                else:
                    txt += chr(char_ord)
            except:
                pass

        KB.kbipW.activateWindow()
        KB.kbipW.kbip.setText(txt)
        KB.kbipW.kbip.setFocus()

    def kb_disp(self, event):

        self.lower_flag = 1
        self.caps_bt.setIcon(QIcon(QPixmap("designs\icons\caps off.png")))
        for button in self.buttons:
            button.setText(button.text().lower())

        KB.kbui.setCurrentWidget(KB.alpW)
        KB.kbui.hide()
        KB.kbipW.hide()
        KB.kbui.show()
        KB.kbipW.show()
        KB.kbipW.kbip.setMaxLength(32767)
        KB.kbipW.kbip.setEchoMode(QLineEdit.Normal)

        if ui.mmW.Password_ip.hasFocus():
            KB.kbipW.kbip.setEchoMode(QLineEdit.Password)    
            KB.kbipW.kbip.setText(ui.mmW.Password_ip.text())
            self.LE = ui.mmW.Password_ip

        elif ui.smscW.Msg_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.smscW.Msg_ip.toPlainText())
            self.LE = ui.smscW.Msg_ip

        elif ui.pssW.Hd1_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Hd1_ip.text())
            self.LE = ui.pssW.Hd1_ip

        elif ui.pssW.Hd2_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Hd2_ip.text())
            self.LE = ui.pssW.Hd2_ip

        elif ui.pssW.Hd3_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Hd3_ip.text())
            self.LE = ui.pssW.Hd3_ip

        elif ui.pssW.Ft1_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Ft1_ip.text())
            self.LE = ui.pssW.Ft1_ip

        elif ui.pssW.Ft2_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Ft2_ip.text())
            self.LE = ui.pssW.Ft2_ip

        elif ui.pssW.Ft3_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.pssW.Ft3_ip.text())
            self.LE = ui.pssW.Ft3_ip

###################################################################################


class NumpadWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NumpadWindow.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)

        self.names = ['1', '2', '3', '4', '5', '6',
                      '7', '8', '9', '0', '.', ',', '/', '-', '*']
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
        # ui.haptic_flag = 1
        txt = KB.kbipW.kbip.text()

        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            KB.kbui.hide()
            KB.kbipW.hide()
            self.LE.setText(txt)

        else:
            txt += chr(char_ord)

        KB.kbipW.kbip.setText(txt)
        KB.kbipW.activateWindow()
        KB.kbipW.kbip.setFocus()

    def kb_disp(self, event):

        KB.kbui.setCurrentWidget(KB.npW)
        KB.kbui.hide()
        KB.kbipW.hide()
        KB.kbui.show()
        KB.kbipW.show()
        KB.kbipW.kbip.setMaxLength(32767)
        KB.kbipW.kbip.setEchoMode(QLineEdit.Normal)


        if ui.wcW.Mc_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.wcW.Mc_ip.text())
            self.LE = ui.wcW.Mc_ip

        elif ui.wcW.Cc_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.wcW.Cc_ip.text())
            self.LE = ui.wcW.Cc_ip

        elif ui.hcW.RefH_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.hcW.RefH_ip.text())
            self.LE = ui.hcW.RefH_ip

        elif ui.smscW.Mbno_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.smscW.Mbno_ip.text())
            KB.kbipW.kbip.setMaxLength(10)
            self.LE = ui.smscW.Mbno_ip

        elif ui.ssmsW.Mbno_ip.hasFocus():
            KB.kbipW.kbip.setText(ui.ssmsW.Mbno_ip.text())
            KB.kbipW.kbip.setMaxLength(10)
            self.LE = ui.ssmsW.Mbno_ip

#############################################################################################


class NumbersandSymbolsWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NumberandSymbolsWindow.ui", self)
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)
        self.names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '/',
                      ':', '~', '(', ')', '$', '&', "'", '"', '+', '@', '.', ',',
                      '?', '!', '#', '%', '*']

        self.buttons = [self.one_bt, self.two_bt, self.three_bt, self.four_bt, self.five_bt, self.six_bt, self.seven_bt, self.eight_bt,
                        self.nine_bt, self.zero_bt, self.hyphen_bt, self.fslash_bt, self.colon_bt, self.tilde_bt, self.ob_bt, self.cb_bt,
                        self.dollar_bt, self.and_bt, self.sapostrophe_bt, self.dapostrophe_bt, self.plus_bt, self.at_bt, self.dot_bt,
                        self.comma_bt, self.qmark_bt, self.excmark_bt, self.hash_bt, self.percentage_bt, self.star_bt]
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
        KB.kbui.setCurrentWidget(KB.alpW)

    def buttonClicked(self, char_ord):
        # ui.haptic_flag = 1

        txt = KB.kbipW.kbip.text()

        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:
            KB.kbui.hide()
            KB.kbipW.hide()
            KB.alpW.LE.setText(txt)

        else:
            txt += chr(char_ord)

        KB.kbipW.kbip.setText(txt)
        KB.kbipW.activateWindow()
        KB.kbipW.kbip.setFocus()

###################################################################################
###################################################################################


class UI():
    def __init__(self):
        self.widget = QStackedWidget()
        self.widget.setWindowFlag(Qt.FramelessWindowHint)
        # Instances of windows
        self.InsertW = InsertWindow()
        self.vidAdW = VideoAdDisplayWindow()
        self.mmW = MainMenu()
        self.OptionsW = SettingsOptions()
        self.setupW = SetupWindow()
        self.wcW = WCWindow()
        self.hcW = HCWindow()
        self.smscW = SMSCWindow()
        self.rW = RWindow()
        self.dW = DiagWindow()
        self.pssW = PSSWindow()
        self.bmiW = BMI()
        self.bmiwwdW = BMIWWD()
        self.posW = POSWindow()
        self.ssmsW = SendSMSWindow()
        self.imgAdW = ImageAdDisplayWindow()
        self.gdapW = GetDownAPWindow()
        self.gdW = GetDownWindow()
        self.npW = NoPaperWindow()

        # widgets list
        self.widgets_list = [self.InsertW, self.vidAdW, self.mmW,
                             self.OptionsW, self.setupW, self.wcW, self.hcW,
                             self.smscW, self.rW, self.dW, self.pssW, self.bmiW,
                             self.posW, self.ssmsW, self.imgAdW, self.gdapW, self.gdW,
                             self.npW, self.bmiwwdW]

        for i in self.widgets_list:
            self.widget.addWidget(i)

        # set width and height

        self.widget.setGeometry(640, 140, 600, 1024)
        self.widget.show()
        self.run_ad()

        #  BGM thread
        self.flag = 1
        self.Player = QMediaPlayer()
        # self.click = QMediaPlayer()
        # self.click.setMedia(QMediaContent(QUrl.fromLocalFile(click_sound)))
        self.music = threading.Thread(target=self.loop)
        # self.haptic_flag = 0
        self.music.daemon = True
        self.music.start()

    def run_ad(self):
        if gv.SettingsInputs.value('Screensaver') == 'Videos':
            self.vidAdW.setFocus()
            self.widget.setCurrentWidget(self.vidAdW)
            self.vidAdW.video_run()
        else:
            self.imgAdW.setFocus()
            self.widget.setCurrentWidget(self.imgAdW)
            self.imgAdW.mediaPlayer.play()

    def setandplay_bgm(self, filename):
        self.Player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.stop_bgm()
        self.play_bgm()

    def stop_bgm(self):
        self.flag = 1
        self.Player.stop()

    def play_bgm(self):
        self.flag = 0
        self.Player.play()

    def loop(self):
        while True:
            if self.flag == 0 and self.Player.state() == 0:
                time.sleep(1.5)
                if self.flag == 0:
                    self.Player.play()

            # if self.haptic_flag == 1:
            #     self.click.play()
            #     self.haptic_flag = 0

###################################################################################
###################################################################################


class KeyboardUI():
    def __init__(self):
        self.kbui = QStackedWidget()
        self.kbui.setStyleSheet(
            """QStackedWidget
                                    {
                                    background-color: rgb(35, 35, 35);
                                    border-radius:15px;
                                    }"""
        )
        self.kbui.setGeometry(640, 790, 600, 375)
        self.kbui.setWindowFlag(Qt.FramelessWindowHint)
        self.kbipW = KBIPWindow()
        self.alpW = AlphabetsWindow()
        self.nsW = NumbersandSymbolsWindow()
        self.npW = NumpadWindow()
        self.kbui.addWidget(self.alpW)
        self.kbui.addWidget(self.nsW)
        self.kbui.addWidget(self.npW)

###################################################################################
###################################################################################


class GV():
    def __init__(self):
        self.getSettingsValues()

    def getSettingsValues(self):
        self.SettingsInputs = QSettings('Smart BMI', 'SettingsWindow')

###################################################################################
###################################################################################


# os.system("python img2SS.py")

[background, insertcoin, printM, sms,
 click_sound, insertcoin_tamil,
  printM_tamil, sms_tamil] = ['Sounds/Background.wav', 'Sounds/InsertCoin.mp3','Sounds/Print.mp3',
                                'Sounds/sms.mp3', 'Sounds/kbclick.wav', 'Sounds\insertcoin_tamil.mp3',
                                'Sounds\Print_tamil.mp3', 'Sounds\sms_tamil.mp3']

gv = GV()

###################################################################################
###################################################################################
# Application

app = QApplication(sys.argv)
KB = KeyboardUI()
ui = UI()
app.exec_()

###################################
###################################
