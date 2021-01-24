import time
import numpy as np
from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import QApplication, QColor, QPainter, QPen, QWidget, Qt
from PyQt5.uic import loadUi
from common_define import *
from least_sq_calibration import *

class DrawFiveRects(QWidget):
    def __init__(self,parent):
        super().__init__()
        # Use secondary screen
        desktop = QApplication.desktop()
        self.setGeometry(desktop.screenGeometry(CAL_DISP_NUM))
        self.setWindowTitle('Calibration Display')
        self.setStyleSheet("background-color:black;")
        self.parent = parent
        self.current_x = None
        self.current_y = None
    
    def paintEvent(self,event):
        painter = QPainter()
        painter.begin(self)
        self.drawRectangles(painter)
        painter.end()
        
    def drawRectangles(self,painter):
        painter.setPen(QPen(Qt.red,2,Qt.NoPen))
        painter.setBrush(QColor(255,0,0))
        size = self.size()
        x_offset = int(size.width()/6)
        y_offset = int(size.height()/6)
        if self.parent.calibration_point_flag == 0:
            pass
        elif self.parent.calibration_point_flag == 1:
            self.current_x,self.current_y = 1*x_offset,3*y_offset
            painter.drawRect(1*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.calibration_point_flag == 2:
            self.current_x,self.current_y = 3*x_offset,3*y_offset
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.calibration_point_flag == 3:
            self.current_x,self.current_y = 5*x_offset,3*y_offset
            painter.drawRect(5*x_offset-CAL_SQUARE_LENGTH,3*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.calibration_point_flag == 4:
            self.current_x,self.current_y = 3*x_offset,1*y_offset
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,1*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        elif self.parent.calibration_point_flag == 5:
            self.current_x,self.current_y = 3*x_offset,5*y_offset
            painter.drawRect(3*x_offset-CAL_SQUARE_LENGTH,5*y_offset-CAL_SQUARE_LENGTH,
                CAL_SQUARE_LENGTH,CAL_SQUARE_LENGTH)
        else:
            pass

class cali_control(QDialog):
    def __init__(self,parent):
        super(cali_control,self).__init__()
        loadUi('./ui/cali_control.ui',self)
        self.parent = parent
        self.calibration_point_flag = 0
        self.cali_display = DrawFiveRects(self)
        self.vec_array = np.empty(shape=[0,4])
        
        # Button control
        self.btnCal_1.clicked.connect(self.show_cali_display_1)
        self.btnCal_2.clicked.connect(self.show_cali_display_2)
        self.btnCal_3.clicked.connect(self.show_cali_display_3)
        self.btnCal_4.clicked.connect(self.show_cali_display_4)
        self.btnCal_5.clicked.connect(self.show_cali_display_5)
        self.btnDoCalibration.clicked.connect(self.do_data_collection)
        self.btnCompute.clicked.connect(self.do_calibration)

    # Calibration function
    def do_data_collection(self):
        for i in range(CAL_SAMPLE_SIZE):
            self.vec_array = np.append(self.vec_array,[
                [self.parent.parent.pcr_vec[0],self.parent.parent.pcr_vec[1],
                self.cali_display.current_x,self.cali_display.current_y,]
                ],axis=0)
            time.sleep(CAL_SAMPLE_INTV)
    
    def do_calibration(self):
        # Do least square calibration
        self.parent.parent.coeff = least_sq_calibration(self.vec_array)
        # Enable buttons on main window
        self.parent.parent.btnStart.setEnabled(True)
        self.parent.parent.btnValidation.setEnabled(True)
        # Close window
        self.cali_display.close()
        self.close()

    # Need to be simplified
    def show_cali_display_1(self):
        self.calibration_point_flag = 1
        self.cali_display.showFullScreen()
    
    def show_cali_display_2(self):
        self.calibration_point_flag = 2
        self.cali_display.showFullScreen()
    
    def show_cali_display_3(self):
        self.calibration_point_flag = 3
        self.cali_display.showFullScreen()
    
    def show_cali_display_4(self):
        self.calibration_point_flag = 4
        self.cali_display.showFullScreen()
    
    def show_cali_display_5(self):
        self.calibration_point_flag = 5
        self.cali_display.showFullScreen()