import cv2
import os
import glob
import numpy as np

class CameraHandler:
    """
    一个用于处理摄像头操作的类。

    ...

    属性
    ----------
    cameras : list
        所有已连接的USB摄像头的列表

    方法
    -------
    check_cameras():
        检查所有摄像头是否成功打开。
    capture_all():
        从所有摄像头捕获图像并保存到指定目录。
    capture_single(box_id):
        从指定摄像头捕获图像并保存到指定目录。
    close_cameras():
        关闭所有摄像头。
    """

    def __init__(self):
        """
        构造CameraHandler对象所需的所有必要属性。

        ...

        属性
        ----------
        cameras : list
            所有已连接的USB摄像头的列表
        """
        self.cameras = [cv2.VideoCapture(i) for i in range(4)]

    def check_cameras(self):
        """
        检查所有摄像头是否成功打开。
        """
        for camera in self.cameras:
            if not camera.isOpened():
                print(f"无法打开摄像头 {self.cameras.index(camera)}")

    def capture_all(self):
        """
        从所有摄像头捕获图像并保存到指定目录。
        """
        for index in range(len(self.cameras)):
            self.capture_single(index + 1)

    def capture_single(self, box_id):
        """
        从指定摄像头捕获图像并保存到指定目录。

        参数
        ----------
        box_id : int
            要从中捕获图像的箱子（摄像头）的id。
        """
        camera = self.cameras[box_id - 1]
        ret, frame = camera.read()  # 读取一帧图像
        if ret:
            # 保存全照片
            full_image_filename = f"data/pics/{box_id}/full_img.jpg"
            os.makedirs(os.path.dirname(full_image_filename), exist_ok=True)
            cv2.imwrite(full_image_filename, frame)

            # 将图像平均分割为四份
            height, width, _ = frame.shape
            quarter_height = height // 2
            quarter_width = width // 2
            img_parts = [
                frame[0:quarter_height, 0:quarter_width],
                frame[0:quarter_height, quarter_width:width],
                frame[quarter_height:height, 0:quarter_width],
                frame[quarter_height:height, quarter_width:width]
            ]

            # 存储分割的四个照片
            for part_index, img_part in enumerate(img_parts):
                filename = f"data/pics/{box_id}/img_part_{part_index}.jpg"
                cv2.imwrite(filename, img_part)
        else:
            print(f"未能从摄像头 {box_id} 读取图像")
        self.close_cameras()

    def close_cameras(self):
        """
        关闭所有摄像头。
        """
        for camera in self.cameras:
            camera.release()