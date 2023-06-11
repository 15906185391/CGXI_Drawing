import cv2.cv2 as cv
import numpy as np


class Trans():
    def __init__(self):
        self.image_points_3D = np.array([
            (0, 0, 0),
            (0, 512, 0),
            (512, 512, 0),
            (512, 0, 0)
        ], dtype="double")
        self.image_points_2D = np.array([
            (-440, 190),
            (-293, 342),
            (-443, 490),
            (-587, 341)
        ], dtype="double")
        self.distortion_coeffs = np.zeros((4, 1))
        self.focal_length = 1
        self.center = (256, 256)
        self.matrix_camera = np.array(
            [[self.focal_length, 0, self.center[0]],
             [0, self.focal_length, self.center[1]],
             [0, 0, 1]], dtype="double"
        )
        self.success, self.vector_rotation, self.vector_translation = cv.solvePnP(objectPoints=self.image_points_3D,
                                                                                  imagePoints=self.image_points_2D,
                                                                                  cameraMatrix=self.matrix_camera,
                                                                                  distCoeffs=None, flags=0)
        # print(self.vector_rotation)
        # print(self.vector_translation)

    def transform(self, point, z):
        trans_point, _ = cv.projectPoints(point, self.vector_rotation, self.vector_translation, self.matrix_camera,
                                          None)
        z_ = [z, 0, 0, 0]
        trans_point = np.append(trans_point[0], z_)
        # trans_point=np.round(trans_point,3)
        return trans_point


# trans = Trans()
# point = trans.transform(np.array([495.0, 198.0, 0.0]), 1)
# print(point)
