import os
import cv2
import numpy as np
import pytesseract

from LgbConfig import ADB_DEVICE_SERIAL
from utils.adb import PyADB
from utils.find_ansers import FindAnswers

class ADBOCR:
    def __init__(self) -> None:
        import jieba
        jieba.lcut('dasdsafsamfdsam', cut_all=False)
        # adb 初始化
        self.adb = PyADB(ADB_DEVICE_SERIAL)
        self.find_answers = FindAnswers()

    def identify(self, img, context_coordinate):
        img_gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
        img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        xmin, ymin, xmax, ymax = context_coordinate
        img_thresh = img_thresh[ymin:ymax, xmin:xmax].copy()
        text = pytesseract.image_to_string(img_thresh, lang='chi_sim').replace('\n', '')
        return text

    def answer(self):
        xmin, ymin, xmax, ymax = 50, 700, 1030, 1100  # 题目框
        context_coordinate = (xmin, ymin, xmax, ymax)
        img_rgb = self.adb.screencap()
        context = self.identify(img_rgb, context_coordinate)
        if len(context) > 90:
            context = context[:90]
        print('识别文字: ',context)
        res = self.find_answers.get_result('未知', context, ['未知', '未知'])
        print("正常查找：", res)
        self.find_answers.find_jieba(context)
        

    def main(self, user, passwd):
        while True:
            if input("等待下一轮:").upper() == 'Q':
                break
            os.system("cls")
            self.answer()
            