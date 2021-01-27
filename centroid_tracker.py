import cv2
import numpy as np


class centroid_tracker(object):
    def __init__(self,parent):
        self.parent = parent
    
    def track(self):
        cr_center = np.empty(2)
        pupil_center = np.empty(2)
        cr_thres = self.parent.cr_min
        pupil_thres = self.parent.pupil_max
        img = self.parent.image
        cr_mask = cv2.inRange(img,cr_thres,255)
        cr_moment = cv2.moments(cr_mask,True)
        pupil_mask = cv2.inRange(img,0,pupil_thres)
        pupil_moment = cv2.moments(pupil_mask,True)
        cr_center[0],cr_center[1] = np.divide(cr_moment['m10'],cr_moment['m00']),\
                                    np.divide(cr_moment['m01'],cr_moment['m00'])
        pupil_center[0],pupil_center[1] = np.divide(pupil_moment['m10'],pupil_moment['m00']),\
                                        np.divide(pupil_moment['m01'],pupil_moment['m00'])
        pcr_vec = pupil_center-cr_center
        self.parent.pcr_vec = pcr_vec
        self.parent.pupil_center = pupil_center
        self.parent.cr_center = cr_center
        polynominal = np.array([
            1,pcr_vec[0],pcr_vec[1],pcr_vec[0]*pcr_vec[1],pcr_vec[0]**2,pcr_vec[1]**2
        ])

        if self.parent.coeff is not None:
            self.parent.gaze_point[0] = np.matmul(polynominal,self.parent.coeff[:,0]).item()
            self.parent.gaze_point[1] = np.matmul(polynominal,self.parent.coeff[:,1]).item()