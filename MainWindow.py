# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowRsPyRk.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGroupBox, QLabel,
                               QMainWindow, QMenuBar, QPushButton, QSizePolicy,
                               QStatusBar, QWidget, QHBoxLayout, QVBoxLayout)
import numpy as np
# import matplotlib
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import axes3d
#
# matplotlib.use("QtAgg")
QT_API = 'PySide6'
# from matplotlib.backends.backend_qt5agg import FigureCanvas


class Ui_MainWindow(object):
    def __init__(self):
        self.layout = None
        self.column_names = ["Column A", "Column B", "Column C"]
        # self.X, self.Y, self.Z = axes3d.get_test_data(0.03)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)

        # self.fig = Figure(figsize=(6, 6))
        # self.canvas = FigureCanvas(self.fig)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(10, 40, 720, 600))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(760, 20, 200, 200))
        self.pushButton_OpenCamera = QPushButton(self.groupBox)
        self.pushButton_OpenCamera.setObjectName(u"pushButton_OpenCamera")
        self.pushButton_OpenCamera.setGeometry(QRect(10, 30, 75, 30))
        self.pushButton_CloseCamera = QPushButton(self.groupBox)
        self.pushButton_CloseCamera.setObjectName(u"pushButton_CloseCamera")
        self.pushButton_CloseCamera.setGeometry(QRect(110, 30, 75, 30))
        self.pushButton_Preview = QPushButton(self.groupBox)
        self.pushButton_Preview.setObjectName(u"pushButton_Preview")
        self.pushButton_Preview.setGeometry(QRect(10, 90, 75, 30))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(180, 700, 53, 15))
        self.label_FPS = QLabel(self.centralwidget)
        self.label_FPS.setObjectName(u"label_FPS")
        self.label_FPS.setGeometry(QRect(250, 700, 53, 15))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(770, 300, 200, 200))
        self.pushButton_OpenRobot = QPushButton(self.groupBox_2)
        self.pushButton_OpenRobot.setObjectName(u"pushButton_OpenRobot")
        self.pushButton_OpenRobot.setGeometry(QRect(10, 30, 75, 30))
        self.pushButton_Draw = QPushButton(self.groupBox_2)
        self.pushButton_Draw.setObjectName(u"pushButton_Draw")
        self.pushButton_Draw.setGeometry(QRect(110, 30, 75, 30))
        self.pushButton_shutdown = QPushButton(self.groupBox_2)
        self.pushButton_shutdown.setObjectName(u"pushButton_shutdown")
        self.pushButton_shutdown.setGeometry(QRect(110, 80, 75, 30))
        self.pushButton_poweroff = QPushButton(self.groupBox_2)
        self.pushButton_poweroff.setObjectName(u"pushButton_poweroff")
        self.pushButton_poweroff.setGeometry(QRect(10, 80, 75, 30))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.layout = QHBoxLayout(self.centralwidget)
        # self.layout.addWidget(self.graphicsView)
        # self.layout.addWidget(self.canvas)
        #
        # self.fig.set_canvas(self.canvas)
        #
        # self._ax = self.canvas.figure.add_subplot(projection="3d")
        #
        # self._ax.set_xlabel(self.column_names[0])
        # self._ax.set_ylabel(self.column_names[1])
        # self._ax.set_zlabel(self.column_names[2])
        # self._ax.set_xlim(-500, -400)
        # self._ax.set_ylim(350, 500)
        # self._ax.set_zlim(5, 20)
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u76f8\u673a\u63a7\u5236", None))
        self.pushButton_OpenCamera.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u76f8\u673a", None))
        self.pushButton_CloseCamera.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u6444\u7167\u7247", None))
        self.pushButton_Preview.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8\u6548\u679c", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"FPS:", None))
        self.label_FPS.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u673a\u5668\u4eba\u63a7\u5236", None))
        self.pushButton_OpenRobot.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u673a", None))
        self.pushButton_Draw.setText(QCoreApplication.translate("MainWindow", u"\u7ed8\u5236", None))
        self.pushButton_shutdown.setText(QCoreApplication.translate("MainWindow", u"\u5173\u673a", None))
        self.pushButton_poweroff.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u7535", None))

    # retranslateUi
    # @property
    # def ax(self):
    #     return self._ax
