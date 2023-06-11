import cgxiapi

import time

robotHandle = 1
ipAddr = "192.168.6.6"
port = 2323
passwd = "123"
re1 = cgxiapi.cr_create_robot(robotHandle, ipAddr, port, passwd)  # 建立连接
print("机械臂建立连接返回值：", re1[0].value, re1[1].value)
robotHandle = re1[1].value
file = open('D:\\Users\\kuanli\\Desktop\\Robot\\2.crscript', encoding='utf-8')  ##打开路径
programfile = file.read()  ##读取文件内容
time.sleep(5)
result = cgxiapi.cr_downloadProgram(robotHandle, programfile)  ##加载脚本程序
print("调用结果：", result.value)
time.sleep(3)

result1 = cgxiapi.cr_play(robotHandle)  ##运行程序
print("程序运行结果：", result1.value)
result = cgxiapi.cr_get_robotMoveStatus(robotHandle)  # 判断是否运动完成
print(result[1].value)
# time.sleep(120)
# result2=cgxiapi.cr_stop(robotHandle)