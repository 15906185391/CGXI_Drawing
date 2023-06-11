import gxipy as gx
import time
import threading
import cv2.cv2 as cv

rawImageUpdateList = []
rawImageUpdate = None
rgb_image = None
num = 0


def capture_callback(raw_image):
    global rawImageUpdateList, num, rawImageUpdate, rgb_image
    rgb_image = raw_image.convert("RGB")
    # rgb_image.image_improvement(0,-20,100)
    rgb_image.brightness(75)
    rgb_image.contrast(-20)
    rawImageUpdate = rgb_image.get_numpy_array()
    if len(rawImageUpdateList) == 0:
        rawImageUpdateList.append(rawImageUpdate)
    else:
        rawImageUpdateList.pop()
        rawImageUpdateList.append(rawImageUpdate)
    num += 1


def Save_img():
    img = rawImageUpdateList[0]
    # cv.imwrite("img.jpg", img)


class DahengCamera:
    def __init__(self):
        self.cam = None  # 相机对象
        self.dev_num = None
        self.dev_info_list = None
        self.device_manager = gx.DeviceManager()
        self.AcquisitionThread = None
        self.AcquisitionThreadNeedBeStop = False
        self.IsCameraOpened = False
        self.IsCameraStartAcq = False

    def OpenCamera(self, Index):
        if self.dev_num == 0:
            return False
        elif self.IsCameraOpened:
            return True
        else:
            self.cam = self.device_manager.open_device_by_index(Index)
            self.cam.UserSetSelector=1
            # print(self.cam)
        self.AcquisitionThread = threading.Thread(target=self.AcquisitionThreadFunc_CallBack, args=(), daemon=True)
        self.AcquisitionThread.start()
        self.IsCameraOpened = True
        self.AcquisitionThreadNeedBeStop = False

        return True

    def set_Camera(self):
        # print(self.cam)
        self.cam.GainAuto = 1
        # self.cam.ExposureTime.set(10000.0)
        self.cam.BalanceWhiteAuto = 1
        # self.cam.PixelFormat = "BAYER_GB8"
        self.cam.DeviceLinkThroughputLimitMode = 0
        self.cam.AutoExposureTimeMax = 10000

    def AcquisitionThreadFunc_CallBack(self):
        self.cam.data_stream[0].register_capture_callback(capture_callback)

        while not self.AcquisitionThreadNeedBeStop:
            time.sleep(1)

    def CloseCamera(self, index):
        if not self.IsCameraOpened:
            return

        self.AcquisitionThreadNeedBeStop = True
        self.StopAcquisition()
        time.sleep(0.1)
        self.cam.data_stream[0].unregister_capture_callback()
        self.cam.close_device()
        self.IsCameraOpened = False

    def StartAcquisition(self):
        if self.IsCameraOpened and not self.IsCameraStartAcq:
            self.cam.stream_on()
            self.IsCameraStartAcq = True
        else:
            return

    def StopAcquisition(self):
        if self.IsCameraOpened and self.IsCameraStartAcq:
            self.cam.stream_off()
            self.IsCameraStartAcq = False
        else:
            return

    def GetFPS(self):
        return self.cam.CurrentAcquisitionFrameRate.get()
