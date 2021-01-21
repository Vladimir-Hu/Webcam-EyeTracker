from PyQt5.Qt import QColor, QPainter, QPen, QWidget
from PyQt5.Qt import *
from common_define import *

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