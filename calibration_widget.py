import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.Qt import QImage, QPixmap, QTimer
from calibration_control import *

class calibration_widget(QWidget):
    def __init__(self,parent):
        super(calibration_widget,self).__init__()
        loadUi('./ui/calibration.ui',self)
        self.parent = parent
        # Private variable
        self.cali_control = cali_control(self)
        # UI function
        self.slidePupilMax.setValue(self.parent.pupil_max)
        self.slideCRMin.setValue(self.parent.cr_min)
        self.slidePupilMax.valueChanged.connect(self.set_pupil_threshold)
        self.slideCRMin.valueChanged.connect(self.set_cr_threshold)
        self.btnCalibrate.clicked.connect(self.start_cali_display)
        self.btnExit.clicked.connect(self.close)
        # Update preview
        self.timer_calpreview = QTimer(self)
        self.timer_calpreview.timeout.connect(self.cali_preview)
    
    def start_cali_display(self):
        # Start tracker here
        self.parent.tracker_thread.start()
        self.cali_control.show()

    def set_pupil_threshold(self):
        self.parent.pupil_max = self.slidePupilMax.value()

    def set_cr_threshold(self):
        self.parent.cr_min = self.slideCRMin.value()

    def cali_preview(self):
        pupil_mask = np.expand_dims(cv2.inRange(self.parent.image,0,self.parent.pupil_max), axis=2)
        cr_mask = np.expand_dims(cv2.inRange(self.parent.image,self.parent.cr_min,255),axis=2)
        image = np.multiply(0.70,cv2.cvtColor(self.parent.image,cv2.COLOR_GRAY2RGB))
        image = image.astype(np.uint8)
        temp_zero = np.expand_dims(np.zeros_like(self.parent.image),axis=2)
        # Red cr & Blue pupil
        pupil_mask = np.concatenate((temp_zero,temp_zero,pupil_mask),axis=-1)
        cr_mask = np.concatenate((cr_mask,temp_zero,temp_zero),axis=-1)
        image = cv2.add(image,pupil_mask)
        image = cv2.add(image,cr_mask)
        # Display image
        qformat = QImage.Format_RGB888
        out_image = QImage(image,image.shape[1],image.shape[0],image.strides[0],qformat)
        self.labCalPreview.setPixmap(QPixmap.fromImage(out_image))
        self.labCalPreview.setScaledContents(True)