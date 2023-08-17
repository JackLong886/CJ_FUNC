import cv2
import numpy as np


def cv_imread(file_path, read_type=-1):
    """解决无法读取中文路径的问题"""
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), read_type)
    return cv_img
