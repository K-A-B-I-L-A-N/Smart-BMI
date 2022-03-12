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
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("Saved videos\Img_SS.avi")))
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.checker)

    def checker(self, state):
        print(state)
        if state == 0:
            self.mediaPlayer.play()

    def keyPressEvent(self, event):
        if event.key() == 65:
            ui.BasicW.Weight_ip.clear()
            self.mediaPlayer.stop()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


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
            ui.BasicW.Weight_ip.clear()
            ui.play_bgm()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

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


###################################################################################

class BasicWindow(QMainWindow):
    def __init__(self):
        # Loading ui
        super().__init__()
        uic.loadUi("UI Files\Mainwindow.ui", self)
        # Button click events, set values
        self.Settings_Bt.clicked.connect(self.gotoMainMenu)
        self.Go_Bt.clicked.connect(self.gotoInsertScreen)
        self.Weight_ip.setValidator(QIntValidator())
        self.Weight_ip.cursorPositionChanged.connect(self.weight_checker)
        self.Weight_ip.mousePressEvent = vkpW.kb_disp

    def weight_checker(self):
        try:
            if float(self.Weight_ip.text()) <= 5:
                if gv.SettingsInputs.value('Screensaver') == 'Videos':
                    ui.stop_bgm()
                    time.sleep(1)
                    ui.widget.setCurrentIndex(ui.widgets_list.index(ui.vidAdW))
                    ui.vidAdW.video_run()
                if gv.SettingsInputs.value('Screensaver') == 'Images':
                    time.sleep(2)
                    ui.widget.setCurrentIndex(ui.widgets_list.index(ui.imgAdW))
                    ui.imgAdW.mediaPlayer.play()

        except:
            pass

    def gotoInsertScreen(self):
        try:
            if float(self.Weight_ip.text()) >= 5:
                self.Weight_ip.clear()
                ui.play_insertcoin()
                ui.widget.setCurrentIndex(ui.widgets_list.index(ui.InsertW))
        except:
            pass

    def gotoMainMenu(self):
        ui.mmW.setFocus()
        self.Weight_ip.clear()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.mmW))

############################################################################


class InsertWindow(QMainWindow):
    def __init__(self):
        # load ui
        super().__init__()
        uic.loadUi("UI Files\InsertWindow.ui", self)
        # button click events
        self.Back_Bt.clicked.connect(self.gotoWeightIPScreen)

    def keyPressEvent(self, event):

        if event.key() == 65:
            reply = QMessageBox.question(None, "Wish", "Do you want to display weight?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                ui.play_background()
                ui.widget.setCurrentIndex(ui.widgets_list.index(ui.bmiW))
                ui.bmiW.countdown()

    def gotoWeightIPScreen(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))


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
        self.Back_bt.clicked.connect(self.gotoBasicWindow)
        self.Password_ip.mousePressEvent = vkbW.kb_disp

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
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))
        self.Password_ip.clear()

    def gotoBasicWindow(self):
        self.Admin_bt.setVisible(False)
        self.Password_ip.clear()
        self.Admin_bt.setVisible(False)
        self.Login_bt.setVisible(False)
        self.Cancel_bt.setVisible(False)
        self.Password_label.setVisible(False)
        self.Password_ip.setVisible(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

####################################################################################


class SettingsOptions(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\SettingsOptions.ui", self)
        self.Lang_cb.setCurrentText(gv.SettingsInputs.value('Language'))
        self.Ad_cb.setCurrentText(gv.SettingsInputs.value('Screensaver'))
        self.Signout_bt.clicked.connect(self.gotoBasicWindow)
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

    def gotoBasicWindow(self):
        ui.mmW.Admin_bt.setVisible(False)
        ui.mmW.Login_bt.setVisible(False)
        ui.mmW.Cancel_bt.setVisible(False)
        ui.mmW.Password_label.setVisible(False)
        ui.mmW.Password_ip.setVisible(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))

    def gotoWCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.wcW))

    def gotoHCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.hcW))

    def gotoSMSCWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.smscW))

    def gotoRWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.rW))

    def gotoDiagWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.dW))

    def gotoPSSWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.pssW))

    def gotoSetupWindow(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.setupW))


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
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))

    def gotoSettingsOptions_Save(self):

        if self.Pos_cb.currentText() == 'Print only':
            gv.SettingsInputs.setValue('Print or SMS', 'Print only')
        elif self.Pos_cb.currentText() == 'SMS only':
            gv.SettingsInputs.setValue('Print or SMS', 'SMS only')
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
        self.Mc_ip.mousePressEvent = vkpW.kb_disp
        self.Cc_ip.mousePressEvent = vkpW.kb_disp

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


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
        self.RefH_ip.mousePressEvent = vkpW.kb_disp

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
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


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
        self.Mbno_ip.setValidator(QIntValidator())
        self.Mbno_ip.mousePressEvent = vkpW.kb_disp
        self.Msg_ip.mousePressEvent = vkbW.kb_disp

    def enable(self):
        self.Dc_bt.setEnabled(True)
        self.Send_bt.setEnabled(True)

    def gotoSettingsOptions(self):
        gv.SettingsInputs.setValue('smscW Mbno', self.Mbno_ip.text())
        gv.SettingsInputs.setValue('smscW Msg', self.Msg_ip.toPlainText())
        self.Dc_bt.setEnabled(False)
        self.Send_bt.setEnabled(False)
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


##############################################################################


class RWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\ReportWindow.ui", self)
        self.Ok_bt.clicked.connect(self.gotoSettingsOptions)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


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
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


###############################################################################


class PSSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\PrintSlipSettingsWindow.ui", self)
        self.Yes_cb.clicked.connect(self.clicked_yes)
        self.No_cb.clicked.connect(self.clicked_no)
        self.Cancel_bt.clicked.connect(self.gotoSettingsOptions)
        self.Hd1_ip.mousePressEvent = vkbW.kb_disp
        self.Hd2_ip.mousePressEvent = vkbW.kb_disp
        self.Hd3_ip.mousePressEvent = vkbW.kb_disp
        self.Ft1_ip.mousePressEvent = vkbW.kb_disp
        self.Ft2_ip.mousePressEvent = vkbW.kb_disp
        self.Ft3_ip.mousePressEvent = vkbW.kb_disp

    def clicked_yes(self):
        self.No_cb.setChecked(False)

    def clicked_no(self):
        self.Yes_cb.setChecked(False)

    def gotoSettingsOptions(self):
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.OptionsW))


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
            self.Ht = self.Ht[:len(self.Ht) - int(decode[0])] + "." + self.Ht[len(self.Ht) - int(decode[0]):]
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
            self.Wt = self.Wt[:len(self.Wt) - int(decode[0])] + "." + self.Wt[len(self.Wt) - int(decode[0]):]

        except:
            self.Wt = "75"

        return self.Wt

    def get_bmi(self):
        self.BMindex = str("{:.2f}".format(
            float(self.Ht) / ((float(self.Wt) / 100) ** 2)))

        if self.BMindex < "20":
            self.needle_1.setHidden(False)
        elif self.BMindex >= "20" and self.BMindex < "25":
            self.needle_2.setHidden(False)
        elif self.BMindex >= "25" and self.BMindex < "30":
            self.needle_3.setHidden(False)
        elif self.BMindex >= "30" and self.BMindex < "35":
            self.needle_4.setHidden(False)
        else:
            self.needle_5.setHidden(False)

        return self.BMindex

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.secs = 10
            self.timer.stop()
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.posW))
            ui.posW.countdown()
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
        ui.play_printm()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.gdapW))
        ui.gdapW.countdown()

    def SMS(self):
        self.timer_lb.setText("")
        self.timer.stop()
        self.secs = 10
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.ssmsW))

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
        self.Mbno_ip.mousePressEvent = vkpW.kb_disp

    def gotoPOSWindow(self):
        self.Mbno_ip.clear()
        ui.posW.countdown()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.posW))

    def gotogdW(self):
        self.Mbno_ip.clear()
        ui.play_sms()
        ui.widget.setCurrentIndex(ui.widgets_list.index(ui.gdW))
        ui.gdW.countdown()

###################################################################################

class GetDownAPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\GetDownAPWindow.ui", self)
        self.secs = 5

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.timer.stop()
            self.secs = 5
            #################################
            ui.play_background()
            #######################################
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))
        else:
            self.secs -= 1

###################################################################################

class GetDownWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\GetDownWindow.ui", self)
        self.secs = 5

    def countdown(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

    def displayTime(self):
        if self.secs == 0:
            self.timer.stop()
            self.secs = 5
            #################################
            ui.play_background()
            #######################################
            ui.widget.setCurrentIndex(ui.widgets_list.index(ui.BasicW))
        else:
            self.secs -= 1

###################################################################################

class NoPaperWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\NoPaperWindow.ui", self)

#APP
###################################################################################


class VirtualKeyboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(R"UI Files\VirtualKeyboardWindow.ui", self)
        self.resize(600,512)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(640, 652)
        self.lower_flag = 1
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)
        self.names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                      '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-', ':', 
                      '@', '+']
        self.buttons = [self.a_bt, self.b_bt, self.c_bt, self.d_bt, self.e_bt, self.f_bt, self.g_bt, self.h_bt,
                        self.i_bt, self.j_bt, self.k_bt, self.l_bt, self.m_bt, self.n_bt, self.o_bt, self.p_bt,
                        self.q_bt, self.r_bt, self.s_bt, self.t_bt, self.u_bt, self.v_bt, self.w_bt, self.x_bt,
                        self.y_bt, self.z_bt, self.one_bt, self.two_bt, self.three_bt, self.four_bt, self.five_bt,
                        self.six_bt, self.seven_bt, self.eight_bt, self.nine_bt, self.zero_bt, self.dot_bt,
                        self.hyphen_bt, self.colon_bt, self.at_bt, self.plus_bt]
        # clicked functions

        for button, name in zip(self.buttons, self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button, button.KEY_CHAR)

        self.clr_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.clr_bt, Qt.Key_Clear)

        self.caps_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.caps_bt, Qt.Key_CapsLock)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt, Qt.Key_Backspace)

        self.spc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.spc_bt, Qt.Key_Space)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt, Qt.Key_Home)

        # self.kbip.setFocus()

    def buttonClicked(self, char_ord):
        txt = self.kbip.text()

        if char_ord == Qt.Key_Clear:
            txt = ''

        elif char_ord == Qt.Key_CapsLock:
            if self.caps_bt.text() == 'Caps Off':

                self.caps_bt.setText("Caps On")
                for button in self.buttons:
                    button.setText(button.text().upper())

            else:
                self.caps_bt.setText('Caps Off')
                for button in self.buttons:
                    button.setText(button.text().lower())

            if self.lower_flag == 0:
                self.lower_flag = 1

            else:
                self.lower_flag = 0

        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Space:
            txt += ' '

        elif char_ord == Qt.Key_Home:

            self.close()
            self.LE.setText(txt)

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

    def kb_disp(self, event):

        if ui.mmW.Password_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.mmW.Password_ip.text())
            self.show()
            self.LE = ui.mmW.Password_ip

        elif ui.smscW.Msg_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.smscW.Msg_ip.toPlainText())
            self.show()
            self.LE = ui.smscW.Msg_ip

        elif ui.pssW.Hd1_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Hd1_ip.text())
            self.show()
            self.LE = ui.pssW.Hd1_ip

        elif ui.pssW.Hd2_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Hd2_ip.text())
            self.show()
            self.LE = ui.pssW.Hd2_ip

        elif ui.pssW.Hd3_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Hd3_ip.text())
            self.show()
            self.LE = ui.pssW.Hd3_ip

        elif ui.pssW.Ft1_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Ft1_ip.text())
            self.show()
            self.LE = ui.pssW.Ft1_ip

        elif ui.pssW.Ft2_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Ft2_ip.text())
            self.show()
            self.LE = ui.pssW.Ft2_ip

        elif ui.pssW.Ft3_ip.hasFocus():
            self.hide()
            self.kbip.setText(ui.pssW.Ft3_ip.text())
            self.show()
            self.LE = ui.pssW.Ft3_ip

###################################################################################

class VirtualKeypadWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI Files\VirtualKeypadWindow.ui", self)
        self.resize(600,512)
        self.LE = QLineEdit()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(640, 652)
        self.signalmapper = QSignalMapper()
        self.signalmapper.mapped[int].connect(self.buttonClicked)

        self.names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        self.buttons = [self.one_bt, self.two_bt, self.three_bt, self.four_bt, self.five_bt,
                        self.six_bt, self.seven_bt, self.eight_bt, self.nine_bt, self.zero_bt, 
                        self.dot_bt]

        # clicked functions
        for button, name in zip(self.buttons, self.names):
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalmapper.map)
            self.signalmapper.setMapping(button, button.KEY_CHAR)

        self.clr_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.clr_bt, Qt.Key_Clear)

        self.bckspc_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.bckspc_bt, Qt.Key_Backspace)

        self.done_bt.clicked.connect(self.signalmapper.map)
        self.signalmapper.setMapping(self.done_bt, Qt.Key_Home)


    def buttonClicked(self, char_ord):
        txt = self.kpip.text()

        if char_ord == Qt.Key_Clear:
            txt = ''

        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1]

        elif char_ord == Qt.Key_Home:
            self.close()
            self.LE.setText(txt)

        else:
            txt += chr(char_ord)

        self.kpip.setText(txt)
        self.kpip.setFocus()

    def kb_disp(self, event):

        if ui.BasicW.Weight_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.BasicW.Weight_ip.text())
            self.show()
            self.LE = ui.BasicW.Weight_ip

        elif ui.wcW.Mc_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.wcW.Mc_ip.text())
            self.show()
            self.LE = ui.wcW.Mc_ip

        elif ui.wcW.Cc_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.wcW.Cc_ip.text())
            self.show()
            self.LE = ui.wcW.Cc_ip

        elif ui.hcW.RefH_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.hcW.RefH_ip.text())
            self.show()
            self.LE = ui.hcW.RefH_ip

        elif ui.smscW.Mbno_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.smscW.Mbno_ip.text())
            self.show()
            self.LE = ui.smscW.Mbno_ip

        elif ui.ssmsW.Mbno_ip.hasFocus():
            self.hide()
            self.kpip.setText(ui.ssmsW.Mbno_ip.text())
            self.show()
            self.LE = ui.ssmsW.Mbno_ip

###################################################################################
###################################################################################

class UI():
    def __init__(self):
        self.widget = QStackedWidget()
        # Instances of windows
        self.BasicW = BasicWindow()
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
        self.posW = POSWindow()
        self.ssmsW = SendSMSWindow()
        self.imgAdW = ImageAdDisplayWindow()
        self.gdapW = GetDownAPWindow()
        self.gdW = GetDownWindow()
        self.npW = NoPaperWindow()

        # widgets list
        self.widgets_list = [self.BasicW, self.InsertW, self.vidAdW, self.mmW,
                             self.OptionsW, self.setupW, self.wcW, self.hcW,
                             self.smscW, self.rW, self.dW, self.pssW, self.bmiW,
                             self.posW, self.ssmsW, self.imgAdW, self.gdapW, self.gdW,
                             self.npW]

        for i in self.widgets_list:
            self.widget.addWidget(i)

        # set width and height

        self.widget.setGeometry(640, 140, 600, 1024)
        self.widget.show()

        #  BGM thread
        self.flag = 0
        self.Player = QMediaPlayer()
        self.play_background()
        self.music = threading.Thread(target=self.loop)
        self.music.start()
    
    def play_background(self):
        self.Player.setMedia(QMediaContent(QUrl.fromLocalFile(background)))
        self.stop_and_play()

    def play_insertcoin(self):
        self.Player.setMedia(QMediaContent(QUrl.fromLocalFile(insertcoin)))
        self.stop_and_play()

    def play_printm(self):
        self.Player.setMedia(QMediaContent(QUrl.fromLocalFile(printM)))
        self.stop_and_play()

    def play_sms(self):
        self.Player.setMedia(QMediaContent(QUrl.fromLocalFile(sms)))
        self.stop_and_play()

    def stop_and_play(self):
        self.flag = 1
        self.Player.stop()
        self.Player.play()
        self.flag = 0

    def stop_bgm(self):
        self.flag = 1
        self.Player.stop()

    def play_bgm(self):
        self.flag = 0
        self.Player.play()

    def loop(self):
        while True:
            time.sleep(1)
            if self.flag == 0 and self.Player.state() == 0:
                time.sleep(1.5)
                self.Player.play()

###################################################################################
###################################################################################

class GV():
    def __init__(self):
        self.getSettingsValues()
        os.system('python img2SS.py')

    def getSettingsValues(self):
        self.SettingsInputs = QSettings('Smart BMI', 'SettingsWindow')


gv = GV()
os.system("python img2SS.py")

###################################################################################
###################################################################################

background = 'Sounds/Background.wav'
insertcoin = 'Sounds/InsertCoin.mp3'
printM = 'Sounds/Print.mp3'
sms = 'Sounds/sms.mp3'

###################################################################################
# Application

app = QApplication(sys.argv)
vkbW = VirtualKeyboardWindow()
vkpW = VirtualKeypadWindow()
ui = UI()
app.exec_()

###################################
###################################
