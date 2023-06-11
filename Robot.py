import cgxiapi
import time
from ctypes import *
import basestruct
from Generate_Points import generate_points
from Trans import Trans
import numpy as np
import cv2.cv2 as cv


class Robot:
    def __init__(self):
        self.resOut_area = None
        self.resOut_linear = None
        self.trans = Trans()
        self.my_getPoint = None
        self.img_preview = None
        self.robotHandle = 1
        self.ipAddr = "192.168.6.6"
        self.port = 2323
        self.passwd = "123"
        self.z = -30

    def create_robot(self):
        re1 = cgxiapi.cr_create_robot(self.robotHandle, self.ipAddr, self.port, self.passwd)  # 建立连接
        print("机械臂建立连接返回值：", re1[0].value)
        self.robotHandle = re1[1].value
        time.sleep(0.1)

    def power_on_robot(self):
        cgxiapi.cr_poweron(self.robotHandle)
        while True:
            time.sleep(0.5)
            mode = self.get_robot_Mode()
            # print(mode)
            if mode == 8 or mode == 103:
                break

    def power_off_robot(self):
        cgxiapi.cr_poweroff(self.robotHandle)
        while True:
            time.sleep(0.5)
            mode = self.get_robot_Mode()
            print(mode)
            if mode == 6:
                break

    def shutdown_robot(self):
        cgxiapi.cr_poweroff(self.robotHandle)

    def enable_robot(self):
        cgxiapi.cr_enable(self.robotHandle)
        while True:
            time.sleep(0.5)
            mode = self.get_robot_Mode()
            # print(mode)
            if mode == 103:
                print("Enable")
                break

    def get_robot_Mode(self):
        result = cgxiapi.cr_get_robotMode(self.robotHandle)
        return result[1].value

    def move_robot(self, pose1):
        tarjointpose = [0, 0, 0, 0, 0, 0]
        flangepose = [0, 0, 0, 0, 0, 0]
        pose = pose1
        jointpose = [0, 0, 0, 0, 0, 0]
        tcpMsg = basestruct.TCPMsg()
        py_tcpMsg_pointer_ = byref(tcpMsg)
        cgxiapi.cr_get_currentTCPmsg(self.robotHandle, py_tcpMsg_pointer_)
        cgxiapi.cr_get_jointActualPos(self.robotHandle, jointpose)
        cgxiapi.cr_TcpToFlangePose(pose, tcpMsg.tcpOffset, flangepose)
        cgxiapi.cr_kineInverse(self.robotHandle, flangepose, jointpose, tarjointpose)
        pointControlPara = basestruct.PointControlPara()
        tcpMsg = basestruct.TCPMsg()
        py_tcpMsg_pointer_ = byref(tcpMsg)
        cgxiapi.cr_get_currentTCPmsg(self.robotHandle, py_tcpMsg_pointer_)
        speed = 250  # 速度
        acc = 1500  # 加速度
        pointControlPara.speed = (speed, speed, speed, speed, speed, speed)  # 速度
        pointControlPara.acc = (acc, acc, acc, acc, acc, acc)  # 加速度
        pointControlPara.coordinatePose = (0, 0, 0, 0, 0, 0)  # 参考坐标系位姿
        pointControlPara.jerk = (0, 0, 0, 0, 0, 0)  # 加加速度
        pointControlPara.coordinateType = basestruct.CoordinateType.baseCoordinate  # 坐标系类型
        pointControlPara.pointTransType = basestruct.PointTransType.pointTransStop  # 位置过渡方式
        pointControlPara.pointTransRadius = 0  # 过渡半径
        pointControlPara.poseTranType = basestruct.PoseTranType.poseTranMoveToTargetPose  # 姿态变换方式
        pointControlPara.motiontriggerMode = basestruct.MotiontriggerMode.MovetriggerbyOnlyRpc  # 运动轨迹触发方式
        pointControlPara.tcpOffset = tcpMsg.tcpOffset
        pointControlPara.tcpID = -1
        tarjointpose = (
            tarjointpose[0], tarjointpose[1], tarjointpose[2], tarjointpose[3], tarjointpose[4], tarjointpose[5])
        posetopose = [0, 0, 0, 0, 0, 0]  # 目标位姿
        pose = [0, 0, 0, 0, 0, 0]
        cgxiapi.cr_kineForward(self.robotHandle, tarjointpose, pose)
        cgxiapi.cr_poseTrans(pose, tcpMsg.tcpOffset, posetopose)
        pointControlPara.jointpos = (
            tarjointpose[0], tarjointpose[1], tarjointpose[2], tarjointpose[3], tarjointpose[4], tarjointpose[5])
        pointControlPara.pose = (
            posetopose[0], posetopose[1], posetopose[2], posetopose[3], posetopose[4], posetopose[5])
        cgxiapi.cr_moveL(self.robotHandle, pointControlPara)  # 调用MoveL函数接口
        while True:
            result = cgxiapi.cr_get_robotMoveStatus(self.robotHandle)  # 判断是否运动完成
            if result[1].value == 1:
                break
        while True:
            result = cgxiapi.cr_get_robotMoveStatus(self.robotHandle)  # 判断是否运动完成
            if result[1].value == 0:
                print("机械臂运动至指定位置：", pose1)
                break

    def get_tcp(self, pose=None):
        if pose is None:
            pose = [0, 0, 0, 0, 0, 0]
        cgxiapi.cr_get_tcpActualPose(self.robotHandle, pose)
        return pose

    def get_kineInverse(self, pose):
        tarjointpose = [0, 0, 0, 0, 0, 0]
        flangepose = [0, 0, 0, 0, 0, 0]
        pose = pose
        jointpose = [0, 0, 0, 0, 0, 0]
        tcpMsg = basestruct.TCPMsg()
        py_tcpMsg_pointer_ = byref(tcpMsg)
        cgxiapi.cr_get_currentTCPmsg(self.robotHandle, py_tcpMsg_pointer_)
        cgxiapi.cr_get_jointActualPos(self.robotHandle, jointpose)
        cgxiapi.cr_TcpToFlangePose(pose, tcpMsg.tcpOffset, flangepose)
        cgxiapi.cr_kineInverse(self.robotHandle, flangepose, jointpose, tarjointpose)
        return tarjointpose

    def generate_linear_points(self, resOut_linear):
        resOut_ndarray = np.array(resOut_linear)
        z_ = np.zeros((resOut_ndarray.shape[0], 1), np.double)
        resOut_ndarray = np.append(resOut_ndarray, z_, axis=1)
        b = np.empty([0, 3], np.double)
        trans_point_0 = self.trans.transform(resOut_ndarray[1], self.z + 6)
        trans_point_0_ = [np.array([trans_point_0[0], trans_point_0[1], trans_point_0[2]])]
        b = np.append(b, trans_point_0_, axis=0)
        for i in range(1, resOut_ndarray.shape[0] - 1):
            if resOut_ndarray[i][0] == -1 and resOut_ndarray[i][1] == -1:  # 读取分隔符
                trans_point_1 = self.trans.transform(resOut_ndarray[i - 1], self.z + 6)
                trans_point_1_ = [np.array([trans_point_1[0], trans_point_1[1], trans_point_1[2]])]
                b = np.append(b, trans_point_1_, axis=0)
                trans_point_2 = self.trans.transform(resOut_ndarray[i + 1], self.z + 6)
                trans_point_2_ = [np.array([trans_point_2[0], trans_point_2[1], trans_point_2[2]])]
                b = np.append(b, trans_point_2_, axis=0)
            else:
                trans_point_3 = self.trans.transform(resOut_ndarray[i], self.z)
                trans_point_3_ = [np.array([trans_point_3[0], trans_point_3[1], trans_point_3[2]])]
                b = np.append(b, trans_point_3_, axis=0)
        trans_point_4 = self.trans.transform(resOut_ndarray[-2], self.z + 6)
        trans_point_4_ = [np.array([trans_point_4[0], trans_point_4[1], trans_point_4[2]])]
        b = np.append(b, trans_point_4_, axis=0)
        file_name = str(1) + ".crscript"
        with open(file_name, "w") as f:
            f.writelines("function mainFuncProgram()\n")
            f.writelines("    --start robotConfig\n")
            f.writelines("    TCP_1 = { 2.72, 57.94, 130.874, 49.1144, -173.17, 0 }\n")
            f.writelines("    set_tcp(TCP_1)\n")
            f.writelines("    Payload_1 = { 0, { 0, 0, 0 } }\n")
            f.writelines("    set_tcp_payload(Payload_1[1], Payload_1[2])\n")
            f.writelines("    --end robotConfig\n\n")
            f.writelines("    function RobotProgram()\n")
            f.writelines("        do\n")
            f.writelines("            --Script\n")
            c = b.shape[0]
            f.writelines("            pose_x = {}\n")
            f.writelines("            pose_x={")

            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][0]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][0]))
            f.writelines("}\n")
            f.writelines("            pose_y = {}\n")
            f.writelines("            pose_y={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][1]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][1]))
            f.writelines("}\n")
            f.writelines("            pose_z = {}\n")
            f.writelines("            pose_z={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][2]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][2]))
            f.writelines(" }\n")
            f.writelines("            for i = 1," + str(c + 1) + " do\n")
            f.writelines("                addwaypoint({ pose_x[i],pose_y[i],pose_z[i],0.0,0.0,0.0 })\n")
            f.writelines("            end\n")
            f.writelines("            movel({pose_x[1],pose_y[1],pose_z[1],0.0,0.0,0.0}, 60, 80, 10)\n")
            f.writelines("            movex(2, 40, 20)\n")
            f.writelines("            wait(1)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    RobotProgram_Result = task_create(RobotProgram)\n")
            f.writelines("    function PauseFuncProgram()\n")
            f.writelines("        while (true)\n")
            f.writelines("        do\n")
            f.writelines("            wait(100)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    PauseFuncProgram_Result = task_create(PauseFuncProgram)\n")
            f.writelines("end\n")
            f.writelines("mainFuncProgram_Result = task_create(mainFuncProgram)\n")

    def generate_area_points(self, resOut_area):
        resOut_ndarray = np.array(resOut_area)
        # print(resOut_ndarray)
        self.img_preview = np.zeros((512, 512, 1), np.uint8)
        self.img_preview[:, :, 0] = 255
        for i in range(0, resOut_ndarray.shape[0]):
            if resOut_ndarray[i][0] != -1 and resOut_ndarray[i][1] != -1:  # 读取分隔符
                self.img_preview[int(resOut_ndarray[i][0]), int(resOut_ndarray[i][1]), 0] = 0
        cv.imwrite("img_preview_test.png", self.img_preview)
        z_ = np.zeros((resOut_ndarray.shape[0], 1), np.double)
        resOut_ndarray = np.append(resOut_ndarray, z_, axis=1)
        b = np.empty([0, 3], np.double)
        trans_point_0 = self.trans.transform(resOut_ndarray[1], self.z + 6)
        trans_point_0_ = [np.array([trans_point_0[0], trans_point_0[1], trans_point_0[2]])]
        b = np.append(b, trans_point_0_, axis=0)
        for i in range(1, resOut_ndarray.shape[0] - 2):
            if resOut_ndarray[i][0] == -1 and resOut_ndarray[i][1] == -1:  # 读取分隔符
                trans_point_1 = self.trans.transform(resOut_ndarray[i - 1], self.z + 6)
                trans_point_1_ = [np.array([trans_point_1[0], trans_point_1[1], trans_point_1[2]])]
                b = np.append(b, trans_point_1_, axis=0)
                trans_point_2 = self.trans.transform(resOut_ndarray[i + 1], self.z + 6)
                trans_point_2_ = [np.array([trans_point_2[0], trans_point_2[1], trans_point_2[2]])]
                b = np.append(b, trans_point_2_, axis=0)
            else:
                trans_point_3 = self.trans.transform(resOut_ndarray[i], self.z)
                trans_point_3_ = [np.array([trans_point_3[0], trans_point_3[1], trans_point_3[2]])]
                b = np.append(b, trans_point_3_, axis=0)
        trans_point_4 = self.trans.transform(resOut_ndarray[-2], self.z + 6)
        trans_point_4_ = [np.array([trans_point_4[0], trans_point_4[1], trans_point_4[2]])]
        b = np.append(b, trans_point_4_, axis=0)
        b = np.round(b)
        _, idx = np.unique(b, axis=0, return_index=True)
        b = b[np.sort(idx)]
        file_name = str(2) + ".crscript"
        with open(file_name, "w") as f:
            f.writelines("function mainFuncProgram()\n")
            f.writelines("    --start robotConfig\n")
            f.writelines("    TCP_1 = { 2.72, 57.94, 130.874, 49.1144, -173.17, 0 }\n")
            f.writelines("    set_tcp(TCP_1)\n")
            f.writelines("    Payload_1 = { 0, { 0, 0, 0 } }\n")
            f.writelines("    set_tcp_payload(Payload_1[1], Payload_1[2])\n")
            f.writelines("    --end robotConfig\n\n")
            f.writelines("    function RobotProgram()\n")
            f.writelines("        do\n")
            f.writelines("            --Script\n")
            c = b.shape[0]
            f.writelines("            pose_x = {}\n")
            f.writelines("            pose_x={")

            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][0]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][0]))
            f.writelines("}\n")
            f.writelines("            pose_y = {}\n")
            f.writelines("            pose_y={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][1]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][1]))
            f.writelines("}\n")
            f.writelines("            pose_z = {}\n")
            f.writelines("            pose_z={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][2]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][2]))
            f.writelines(" }\n")
            f.writelines("            for i = 1," + str(c + 1) + " do\n")
            f.writelines("                addwaypoint({ pose_x[i],pose_y[i],pose_z[i],0.0,0.0,0.0 })\n")
            f.writelines("            end\n")
            f.writelines("            movel({pose_x[1],pose_y[1],pose_z[1],0.0,0.0,0.0}, 60, 80, 10)\n")
            f.writelines("            movex(2, 40, 20)\n")
            f.writelines("            wait(1)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    RobotProgram_Result = task_create(RobotProgram)\n")
            f.writelines("    function PauseFuncProgram()\n")
            f.writelines("        while (true)\n")
            f.writelines("        do\n")
            f.writelines("            wait(100)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    PauseFuncProgram_Result = task_create(PauseFuncProgram)\n")
            f.writelines("end\n")
            f.writelines("mainFuncProgram_Result = task_create(mainFuncProgram)\n")

    def generate_points(self):
        self.resOut_linear, self.resOut_area = generate_points()
        self.generate_linear_points(self.resOut_linear)
        self.generate_area_points(self.resOut_area)

    def generate_scripts(self, b):
        file_name = str(b) + ".crscript"
        with open(file_name, "w") as f:
            f.writelines("function mainFuncProgram()\n")
            f.writelines("    --start robotConfig\n")
            f.writelines("    TCP_1 = { 2.72, 57.94, 130.874, 49.1144, -173.17, 0 }\n")
            f.writelines("    set_tcp(TCP_1)\n")
            f.writelines("    Payload_1 = { 0, { 0, 0, 0 } }\n")
            f.writelines("    set_tcp_payload(Payload_1[1], Payload_1[2])\n")
            f.writelines("    --end robotConfig\n\n")
            f.writelines("    function RobotProgram()\n")
            f.writelines("        do\n")
            f.writelines("            --Script\n")
            trans_point_0 = b[0]
            c = b.shape[0]
            f.writelines("            pose_x = {}\n")
            f.writelines("            pose_x={")

            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][0]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][0]))
            f.writelines("}\n")
            f.writelines("            pose_y = {}\n")
            f.writelines("            pose_y={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][1]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][1]))
            f.writelines("}\n")
            f.writelines("            pose_z = {}\n")
            f.writelines("            pose_z={")
            for i in range(0, c):
                if i % 100 == 0:
                    f.writelines("\n\t\t\t")
                f.writelines("[" + str(i + 1) + "]" + "=" + str(b[i][2]) + ",")
            f.writelines("[" + str(c + 1) + "]" + "=" + str(b[c - 1][2]))
            f.writelines(" }\n")
            f.writelines("            for i = 1," + str(c + 1) + " do\n")
            f.writelines("                addwaypoint({ pose_x[i],pose_y[i],pose_z[i],0.0,0.0,0.0 })\n")
            f.writelines("            end\n")
            f.writelines("            movel({pose_x[1],pose_y[1],pose_z[1],0.0,0.0,0.0}, 60, 80, 10)\n")
            f.writelines("            movex(2, 60, 20)\n")
            f.writelines("            wait(1)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    RobotProgram_Result = task_create(RobotProgram)\n")
            f.writelines("    function PauseFuncProgram()\n")
            f.writelines("        while (true)\n")
            f.writelines("        do\n")
            f.writelines("            wait(100)  --sync\n")
            f.writelines("        end\n")
            f.writelines("    end\n")
            f.writelines("    PauseFuncProgram_Result = task_create(PauseFuncProgram)\n")
            f.writelines("end\n")
            f.writelines("mainFuncProgram_Result = task_create(mainFuncProgram)\n")

    def execute_scripts(self):
        for i in range(0, 2):
            file_name = str(i + 1) + ".crscript"
            file = open(file_name, encoding='utf-8')  # 打开路径
            program_file = file.read()  # 读取文件内容

            result = cgxiapi.cr_downloadProgram(self.robotHandle, program_file)  # 加载脚本程序
            print("调用结果：", result.value)
            cgxiapi.cr_play(self.robotHandle)
            while True:
                result = cgxiapi.cr_get_robotMoveStatus(self.robotHandle)  # 判断是否运动完成
                if result[1].value == 1:
                    print("机器人正在运行")
                    break
            while True:
                result = cgxiapi.cr_get_robotMoveStatus(self.robotHandle)  # 判断是否运动完成
                time.sleep(0.5)
                if result[1].value == 0:
                    time.sleep(0.2)
                    result1 = cgxiapi.cr_get_robotMoveStatus(self.robotHandle)
                    if result1[1].value == 0:
                        print("机器人结束运行")
                        break
            trans_point_2 = self.trans.transform(np.array([256.0, 256.0, 0.0]), self.z + 7)
            self.move_robot(trans_point_2)

    def move_robot_to_middle(self):
        pose = self.get_tcp()
        print(pose)
        self.move_robot([pose[0], pose[1], pose[2] + 10, 0, 0, 0])
        trans = Trans()
        trans_point_2 = trans.transform(np.array([256.0, 256.0, 0.0]), self.z + 7)
        self.move_robot(trans_point_2)
        trans_point_1 = trans.transform(np.array([512.0, 512.0, 0.0]), self.z + 7)
        self.move_robot(trans_point_1)
