# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
%matplotlib inline
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(436, 292)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn1_1 = QtWidgets.QPushButton(self.groupBox)
        self.btn1_1.setObjectName("pushButton")
        self.btn1_1.clicked.connect(pushButton_pushedbtn1_1)
        self.btn1_1.setMinimumSize(QtCore.QSize(0, 50))
        self.btn1_1.setObjectName("btn1_1")
        self.verticalLayout_3.addWidget(self.btn1_1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn2_1 = QtWidgets.QPushButton(self.groupBox_2)
        self.btn2_1.setObjectName("pushButton")
        self.btn2_1.clicked.connect(pushButton_pushedbtn2_1)
        self.btn2_1.setMinimumSize(QtCore.QSize(0, 50))
        self.btn2_1.setObjectName("btn2_1")
        self.verticalLayout_4.addWidget(self.btn2_1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btn3_1 = QtWidgets.QPushButton(self.groupBox_3)
        self.btn3_1.setObjectName("pushButton")
        self.btn3_1.clicked.connect(pushButton_pushedbtn3_1)
        self.btn3_1.setMinimumSize(QtCore.QSize(0, 50))
        self.btn3_1.setObjectName("btn3_1")
        self.verticalLayout_5.addWidget(self.btn3_1)
        self.btn3_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.btn3_2.setObjectName("pushButton")
        self.btn3_2.clicked.connect(pushButton_pushedbtn3_2)
        self.btn3_2.setMinimumSize(QtCore.QSize(0, 50))
        self.btn3_2.setObjectName("btn3_2")
        self.verticalLayout_5.addWidget(self.btn3_2)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn4_1 = QtWidgets.QPushButton(self.groupBox_4)
        self.btn4_1.setObjectName("pushButton")
        self.btn4_1.clicked.connect(pushButton_pushedbtn4_1)
        self.btn4_1.setMinimumSize(QtCore.QSize(0, 50))
        self.btn4_1.setObjectName("btn4_1")
        self.verticalLayout_6.addWidget(self.btn4_1)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "1. Stereo"))
        self.btn1_1.setText(_translate("MainWindow", "1.1 Display"))
        self.groupBox_2.setTitle(_translate("MainWindow", "2. Background Subtraction"))
        self.btn2_1.setText(_translate("MainWindow", "2.1 Background Subtraction"))
        self.groupBox_3.setTitle(_translate("MainWindow", "3. Feature Tracking"))
        self.btn3_1.setText(_translate("MainWindow", "3.1 Preprocessing"))
        self.btn3_2.setText(_translate("MainWindow", "3.2 Video Tracking"))
        self.groupBox_4.setTitle(_translate("MainWindow", "4. Augmented Reality"))
        self.btn4_1.setText(_translate("MainWindow", "4.1 Augmented Reality"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F5:
            self.close()


def pushButton_pushedbtn1_1(self):
    imgR = cv2.imread('imR.png',1)
    imgL = cv2.imread('imL.png',1)
    window_size = 9
    min_disp = 13
    num_disp = 109 - min_disp
    blockSize = 14
    uniquenessRatio = 0
    speckleRange = 3
    speckleWindowSize = 0
    disp12MaxDiff = 28
    P1 = 8 * 3 * window_size ** 2
    P2 = 32 * 3 * window_size ** 2
    # stereo = cv2.StereoBM_create(64, 9)
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=blockSize,
        uniquenessRatio=uniquenessRatio,
        speckleRange=speckleRange,
        speckleWindowSize=speckleWindowSize,
        disp12MaxDiff=disp12MaxDiff,
        P1=P1,
        P2=P2
    )
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 8.0
    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp - min_disp) / num_disp)
    # disparity = stereo.compute(imgL,imgR)
    # cv2.imshow('gray', disparity)
    cv2.waitKey()
    cv2.destroyAllWindows()

def pushButton_pushedbtn2_1(self):
    # coding=utf-8
    #from http://zhaoxuhui.top/blog/2017/06/30/%E5%9F%BA%E4%BA%8EPython%E7%9A%84OpenCV%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%8618.html?fbclid=IwAR0qkAOeum09y-qLVA2OxaR_lklV2xo0Y2tWqBH5q_D_oeoRdwxOi7H_kLc
    import cv2

    path = 'bgSub.mp4'

    cap = cv2.VideoCapture(path)

    # 新建一个MOG背景减除对象
    fgbg = cv2.createBackgroundSubtractorKNN()

    # 新建一个卷积核用于开运算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    while 1:
        ret, frame = cap.read()
        if frame is None:
            cv2.waitKey(0)
            break
        else:
            # 应用MOG到每一帧，返回结果是动目标的掩膜
            fgmask = fgbg.apply(frame)
            # 利用开运算进行噪声去除
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

            cv2.imshow('frame', fgmask)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

def pushButton_pushedbtn3_1(self):
    print("btn3_1")

def pushButton_pushedbtn3_2(self):
    print("btn3_2")

def pushButton_pushedbtn4_1(self):
    pam = np.load('cdata.npz')
    mtx = pam['arr_0']
    dist = pam['arr_1']

    objp = np.zeros((11 * 8, 3), np.float32)
    objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2) * 10
    axis = np.float32([[5, 5, 0], [1, 5, 0], [1, 1, 0], [5, 1, 0],
                       [3, 3, -4]]) * 10

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def draw(img, corners, imgpts):
        imgpts = np.int32(imgpts).reshape(-1, 2)


        # draw in red color
        img = cv2.polylines(img, [np.int32(imgpts[0:])], True, tuple([255, 0, 0]), 15, cv2.LINE_AA)
        img = cv2.polylines(img, [np.int32(imgpts[1:])], True, tuple([0, 255, 0]), 15, cv2.LINE_AA)
        img = cv2.polylines(img, [np.int32(imgpts[2:])], True, tuple([0, 0, 255]), 15, cv2.LINE_AA)
        img = cv2.polylines(img, [np.int32(imgpts[:4])], True, tuple([125, 125, 0]), 15, cv2.LINE_AA)

        return img


    for fname in glob.glob("*.bmp"):

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (11, 8), None)
        if ret == True:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Find the rotation and translation vectors.
            ret, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
            # print(ret)

            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

            img = draw(img, corners2, imgpts)
            plt.imshow(img)
            plt.ion()
            plt.pause(1)
            plt.close()

# from PyQt5 import QtWidgets
# from PyQt5 import uic
# from PyQt5.QtGui import QIcon, QPixmap, QClipboard
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QDialog, QBoxLayout, QMainWindow
# from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl, QDir, QMimeData
from PyQt5 import QtWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())