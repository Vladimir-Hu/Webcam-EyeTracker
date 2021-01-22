import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5.Qt import QColor, QPainter, QPainter, QPen, QTimer, Qt
from PyQt5.uic import loadUi
from common_define import *

class DrawValidationRects(QWidget):
    def __init__(self,parent):
        super().__init__()
        # Use secondary screen
        desktop = QApplication.desktop()
        self.setGeometry(desktop.screenGeometry(CAL_DISP_NUM))
        self.setWindowTitle('Validation Display')
        self.setStyleSheet("background-color:black;")
        self.parent = parent
    
    def paintEvent(self,event):
        painter = QPainter()
        painter.begin(self)
        self.drawRectangles(painter)
        painter.end()
        
    def drawRectangles(self,painter):
        painter.setPen(QPen(Qt.blue,CAL_SQUARE_LENGTH))
        if not (np.isnan(self.parent.parent.gaze_point).any()):
            painter.drawPoint(int(self.parent.parent.gaze_point[0].item()),\
                                int(self.parent.parent.gaze_point[1].item()))
        painter.setPen(QPen(Qt.red,2,Qt.NoPen))
        painter.setBrush(QColor(255,0,0))
        size = self.size()
        x_offset = int(size.width()/6)
        y_offset = int(size.height()/6)
        if self.parent.validation_point_flag == 0:
            pass
        elif self.parent.validation_point_flag == 1:
            painter.drawRect(1*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.validation_point_flag == 2:
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.validation_point_flag == 3:
            painter.drawRect(5*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.validation_point_flag == 4:
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,1*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.validation_point_flag == 5:
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,5*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        else:
            pass

class vali_control(QDialog):
    def __init__(self,parent):
        super(vali_control,self).__init__()
        loadUi('./ui/vali_control.ui',self)
        self.parent = parent
        self.validation_point_flag = 0
        self.vali_display = DrawValidationRects(self)
        self.timer_refresh = QTimer(self)
        
        # Button control
        self.btnStart.clicked.connect(self.start_validation)
        self.btnStop.clicked.connect(self.stop_validation)
        self.btnCal_1.clicked.connect(self.show_cali_display_1)
        self.btnCal_2.clicked.connect(self.show_cali_display_2)
        self.btnCal_3.clicked.connect(self.show_cali_display_3)
        self.btnCal_4.clicked.connect(self.show_cali_display_4)
        self.btnCal_5.clicked.connect(self.show_cali_display_5)
    
    # Show validation screen
    def start_validation(self):
        self.vali_display.showFullScreen()
        self.timer_refresh.timeout.connect(self.vali_display.repaint)
        self.timer_refresh.start(20)

    # Exit validation
    def stop_validation(self):
        self.timer_refresh.stop()
        self.vali_display.close()
        self.close()
    
    # Need to be simplified
    def show_cali_display_1(self):
        self.validation_point_flag = 1
    
    def show_cali_display_2(self):
        self.validation_point_flag = 2
    
    def show_cali_display_3(self):
        self.validation_point_flag = 3
    
    def show_cali_display_4(self):
        self.validation_point_flag = 4
    
    def show_cali_display_5(self):
        self.validation_point_flag = 5