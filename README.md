# 智能种植箱（集群） / RemoteFarm

这个项目是一个基于Python的网络应用，允许用户与一个箱子系统进行交互。每个箱子都配备了温度传感器、泵和相机。应用提供了查看当前温度和湿度、刷新箱子相机捕获的图像以及控制泵的功能。
这个项目已经停止维护，仅做存档使用。

This project is a Python-based web application that allows users to interact with a system of boxes. Each box is equipped with a temperature sensor, a pump, and a camera. The application provides functionalities such as viewing the current temperature and humidity, refreshing the image captured by the box's camera, and controlling the pump.
This project is no longer maintained and is for archival use only.

## 硬件信息 / Hardware Information

本系统基于以下硬件设备运行：

- 主设备：树莓派
- 摄像头：任意USB摄像头
- 温湿度传感器：DHT系列传感器

The system runs on the following hardware devices:

- Main device: Raspberry Pi
- Camera: Any USB camera
- Temperature and humidity sensor: DHT series sensor

## 开始 / Getting Started

要在您的本地机器上运行此项目的副本以进行开发和测试，您需要安装Python以及Bottle网络框架。

To get a copy of this project up and running on your local machine for development and testing purposes, you will need Python installed along with the Bottle web framework.

### 先决条件 / Prerequisites

- Python
- Bottle网络框架 / Bottle web framework

### 安装 / Installing

1. 克隆仓库到您的本地机器。/ Clone the repository to your local machine.
2. 使用pip安装所需的依赖项：/ Install the required dependencies using pip:
   ```
   pip install bottle
   ```
   项目内已自带bottle.py，也可不进行该步骤 / Or you can use bottle.py if you cannot install
3. 运行main.py文件以启动服务器：/ Run the main.py file to start the server:
   ```
   python main.py
   ```

## 使用 / Usage

应用提供以下端点：/ The application provides the following endpoints:

- `/`: 主页路由，检查用户是否已登录。如果已登录，它将重定向到查看页面。如果没有，它将返回登录页面。/ The home route that checks if the user is logged in. If logged in, it redirects to the view page. If not, it returns the login page.
- `/login`: 登录路由，验证用户凭据。如果有效，它将设置登录cookies并重定向到查看页面。如果没有，它将返回登录错误页面。/ The login route that validates the user credentials. If valid, it sets the login cookies and redirects to the view page. If not, it returns the login error page.
- `/view`: 查看页面路由，检查用户是否已登录。如果已登录，它将验证令牌并返回查看页面。如果没有，它将重定向到主页。/ The view page route that checks if the user is logged in. If logged in, it validates the token and returns the view page. If not, it redirects to the home page.
- `/logout`: 注销路由，检查用户是否已登录。如果已登录，它将删除登录cookies并返回注销成功页面。如果没有，它将返回注销失败页面。/ The logout route that checks if the user is logged in. If logged in, it deletes the login cookies and returns the logout success page. If not, it returns the logout failed page.
- `/pics/<box_id>/<image_name>`: 获取指定箱子图像的路由。/ Route to get the image of the specified box.
- `/endpoint`: 处理从网络客户端发送的命令的端点路由。它根据收到的命令执行操作。/ Endpoint route that handles commands sent from the web client. It performs actions based on the command received.
