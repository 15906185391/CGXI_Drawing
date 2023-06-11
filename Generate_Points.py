# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import getPoint
import getDaub
import matlab
import cv2
import numpy as np

# 1、这里只是以ocr下的RecognizeBankCard能力为例，其他能力请引入相应类目的包和相关类。包名可参考本文档上方的SDK包名称，能力名可参考对应API文档中的Action参数。例如您想使用通用分割，其文档为https://help.aliyun.com/document_detail/151960.html，可以知道该能力属于分割抠图类目，能力名称为SegmentCommonImage，那么您需要将代码中ocr20191230改为imageseg20191230，将RecognizeBankCard改为SegmentCommonImage。
from alibabacloud_facebody20191230.client import Client
from alibabacloud_facebody20191230.models import GenerateHumanSketchStyleAdvanceRequest
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_tea_openapi.models import Config
import requests


def generate_points():
    # 初始化Config
    config = Config(
        # 2、"YOUR_ACCESS_KEY_ID", "YOUR_ACCESS_KEY_SECRET" 的生成请参考https://help.aliyun.com/document_detail/175144.html
        # 如果您是用的子账号AccessKey，还需要为子账号授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html
        # 您的 AccessKey ID
        access_key_id='LTAI5tPhWVf2xXiEwEbeBLiD',
        # 您的 AccessKey Secret
        access_key_secret='NIGfCKkz2RqUW9xqdJuBUCtpVP3syK',
        # 3、访问的域名。注意：这个地方需要求改为相应类目的域名，参考：https://help.aliyun.com/document_detail/143103.html
        endpoint='facebody.cn-shanghai.aliyuncs.com',
        # 访问的域名对应的region
        region_id='cn-shanghai'
    )

    # 初始化RuntimeObject
    runtime_option = RuntimeOptions()

    try:
        # 场景一：文件在本地
        img = open(r'img.jpg', 'rb')

        # 使用完成之后记得调用img.close()关闭流
        # 场景二，使用任意可访问的url
        # url = 'https://tse2-mm.cn.bing.net/th/id/OIP-C.MJxGpXcJ9WnKvw_RZVKb7gAAAA?pid=ImgDet&rs=1'
        # img = io.BytesIO(ff.read())
        # 4、初始化Request，这里只是以RecognizeBankCard为例，其他能力请使用相应能力对应的类
        request = GenerateHumanSketchStyleAdvanceRequest()
        request.image_urlobject = img

        # 初始化Client
        client = Client(config)
        # 5、调用api，注意，recognize_bank_card_advance需要更换为相应能力对应的方法名。方法名是根据能力名称按照一定规范形成的，如能力名称为SegmentCommonImage，对应方法名应该为segment_common_image_advance。
        response = client.generate_human_sketch_style_advance(request, runtime_option)
        print(response.body.data.image_url)
        res = requests.get(response.body.data.image_url)
        with open('res.png', 'wb') as f:
            f.write(res.content)
            f.close()
        img.close()
        # requests.delete(response.body.data.image_url)

        # 生成线条画轨迹
        my_getPoint = getPoint.initialize()
        my_getDaub = getDaub.initialize()
        fileNameIn = "res.png"
        # 分辨率设置
        resolutionIn = matlab.double([448.0], size=(1, 1))
        kernel_sizeIn = matlab.double([13.0], size=(1, 1))
        resOut_linear, KOut, line_patternOut = my_getPoint.get_point(fileNameIn, resolutionIn, nargout=3)
        resOut_area, area_patternOut = my_getDaub.get_daub(fileNameIn, resolutionIn, kernel_sizeIn, nargout=2)

        # 最终的线条画
        # line_patternOut = np.array(line_patternOut, np.uint8) * 255
        # cv2.namedWindow("line_pattern")
        # cv2.imshow("line_pattern", line_patternOut)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite(r"line_pattern.png", line_patternOut)

        # 线条画轨迹可视化
        # KOut = np.array(KOut, np.uint8) * 255
        # cv2.namedWindow("KOut")
        # cv2.imshow("KOut", line_patternOut)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite(r"KOut.png", line_patternOut)

        my_getPoint.terminate()
        my_getDaub.terminate()
        return resOut_linear, resOut_area

    except Exception as error:
        # 获取整体报错信息
        print(error)
        # 获取单个字段
        print(error.code)
        # tips: 可通过error.__dict__查看属性名称
        img.close()
        return -1
