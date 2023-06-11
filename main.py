import multiprocessing
import sys

import cv2.cv2 as cv
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import DahengCamera
from MainWindow import Ui_MainWindow
from Robot import Robot
np.set_printoptions(threshold=np.inf)


# from matplotlib import animation
# import matplotlib.pyplot as plt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Pos = np.empty(shape=(3, 0), dtype=np.double)
        self.Pos_Z = np.empty(shape=(0, 0), dtype=np.double)
        self.Pos_X = np.empty(shape=(0, 0), dtype=np.double)
        self.Pos_Y = np.empty(shape=(0, 0), dtype=np.double)
        self.pose = None
        self.robot = None
        self.cap = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Camera = DahengCamera.DahengCamera()
        self.TimerForShowImageInGraphicsView = QTimer()
        self.ImageWidthInGraphicsView = 720
        self.scene = QGraphicsScene()

        self.Pos_x = np.empty(shape=(0, 0), dtype=np.double)
        self.Pos_y = np.empty(shape=(0, 0), dtype=np.double)
        self.Pos_z = np.empty(shape=(0, 0), dtype=np.double)

        self.SlotInit()
        self.InitUI()

    """ 初始化槽信号函数"""

    def SlotInit(self):
        self.ui.pushButton_OpenCamera.clicked.connect(self.PB_OpenCamera_clicked)
        self.ui.pushButton_CloseCamera.clicked.connect(self.PB_CloseCamera_clicked)
        self.ui.pushButton_OpenRobot.clicked.connect(self.PB_OpenRobot_clicked)
        self.ui.pushButton_Draw.clicked.connect(self.PB_Draw_clicked)
        self.ui.pushButton_Preview.clicked.connect(self.PB_Preview_clicked)
        self.ui.pushButton_poweroff.clicked.connect(self.PB_PowerOff_Robot_clicked)
        self.ui.pushButton_shutdown.clicked.connect(self.PB_ShutDown_Robot_clicked)
        self.TimerForShowImageInGraphicsView.timeout.connect(self.SlotForShowImageInGraphicsView)

    """ 更新UI界面"""

    def UpdateUI(self):
        self.ui.pushButton_OpenCamera.setDisabled(self.Camera.IsCameraOpened)
        self.ui.pushButton_CloseCamera.setDisabled(not self.Camera.IsCameraOpened)
        self.ui.pushButton_Preview.setDisabled(not self.Camera.IsCameraOpened)

    """ 点击OpenCamera"""

    def PB_OpenCamera_clicked(self):
        self.Camera.OpenCamera(1)
        self.Camera.set_Camera()
        self.Camera.StartAcquisition()
        self.TimerForShowImageInGraphicsView.start(33)
        self.UpdateUI()
        # self.PB_Plot3D_clicked()

    """ 点击CloseCamera"""

    def PB_CloseCamera_clicked(self):
        DahengCamera.Save_img()
        self.showImage.save("img.jpg")
        self.Camera.CloseCamera(1)
        if self.TimerForShowImageInGraphicsView.isActive():
            self.TimerForShowImageInGraphicsView.stop()
        DahengCamera.num = 0
        self.cap = True
        self.UpdateUI()
        self.ui.pushButton_Preview.setDisabled(False)

    def PB_OpenRobot_clicked(self):
        self.robot = Robot()
        self.robot.create_robot()
        self.robot.power_on_robot()
        self.robot.enable_robot()
        self.robot.move_robot_to_middle()
        self.ui.pushButton_Draw.setEnabled(True)

    def PB_PowerOff_Robot_clicked(self):
        self.robot.power_off_robot()

    def PB_ShutDown_Robot_clicked(self):
        self.robot.shutdown_robot()

    def PB_Preview_clicked(self):
        self.robot.generate_points()
        print("正在预览")
        self.img_preview = QImage(self.robot.img_preview.data, self.robot.img_preview.shape[1],
                                  self.robot.img_preview.shape[0],
                                  QImage.Format_Grayscale8)  # 把读取到的视频数据变成QImage形式
        item_preview = QGraphicsPixmapItem(QPixmap.fromImage(self.img_preview))
        self.scene.clear()
        self.scene.addItem(item_preview)
        self.scene.setSceneRect(0, 0, 512, 512)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.show()

    def PB_Draw_clicked(self):
        self.robot.execute_scripts()

    """ 图像显示回调函数"""

    def SlotForShowImageInGraphicsView(self):
        if DahengCamera.rawImageUpdate is None:
            return
        else:
            self.ImageShow = DahengCamera.rawImageUpdateList[0]
            image_width = self.ImageWidthInGraphicsView
            self.show = cv.resize(self.ImageShow, (720, 600))
            # show = cv.cvtColor(show, cv.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            self.showImage = QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                    QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            item = QGraphicsPixmapItem(QPixmap.fromImage(self.showImage))
            self.scene.clear()
            self.scene.addItem(item)
            self.scene.setSceneRect(0, 0, 720, 600)
            self.ui.graphicsView.setScene(self.scene)
            self.ui.graphicsView.show()
            self.ui.label_FPS.setText(str(self.Camera.GetFPS()))

    def InitUI(self):
        self.ui.pushButton_Draw.setDisabled(True)
        self.ui.pushButton_Preview.setDisabled(True)
        self.ui.pushButton_CloseCamera.setDisabled(True)
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
