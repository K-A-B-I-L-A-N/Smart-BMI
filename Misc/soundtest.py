import glob
import os
import sys
import time
import serial
import threading
import serial.tools.list_ports
from PyQt5 import uic,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *


click_sound = 'Sounds/kbclick.wav'
click = QMediaPlayer()
click.setMedia(QMediaContent(QUrl.fromLocalFile(click_sound)))
click.play()
time.sleep(1)
