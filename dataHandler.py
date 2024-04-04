import time
import DHTemp
import camHandler

class Boxes:
    """
    Boxes类负责管理系统中的箱子和用户。

    属性:
        boxConfigPath (str): 箱子配置文件的路径。
        imagePath (str): 图像目录的路径。
        userConfigPath (str): 用户配置文件的路径。
        boxesList (list): 系统中所有箱子的列表。
        userList (list): 系统中所有用户的列表。
    """

    def __init__(self):
        """
        使用配置文件的路径初始化Boxes类，并为箱子和用户创建空列表。
        """
        self.boxConfigPath = './data/boxConfig.json'
        self.imagePath = './data/image/'
        self.userConfigPath = './data/userConfig.json'
        self.boxesList = []
        self.userList = []

        self.importBoxFromJson()
        self.importUserFromJson()

    def importBoxFromJson(self):
        """
        从JSON文件加载箱子配置。
        """
        import json
        with open(self.boxConfigPath, 'r') as file:
            data = json.load(file)
        for box in data:
            self.boxesList.append(Box(box['id'], box['tempSensor'], box['pump'], box['camera']))

    def saveBoxToJson(self):
        """
        将箱子配置保存到JSON文件。
        """
        import json
        data = []
        for box in self.boxesList:
            data.append(str(box))
        with open(self.boxConfigPath, 'w') as file:
            json.dump(data, file)

    def importUserFromJson(self):
        """
        从JSON文件加载用户配置。
        """
        import json
        with open(self.userConfigPath, 'r') as file:
            data = json.load(file)
        for user in data:
            self.userList.append(User(user['username'], user['password'], user['token'], user['expireTime'], user['boxID']))

    def validateUser(self, username, password):
        """
        验证用户的登录凭证。

        参数:
            username (str): 要验证的用户名。
            password (str): 要验证的密码。

        返回:
            bool: 如果凭证有效，则为True，否则为False。
        """
        for user in self.userList:
            if user.username == username:
                return user.validatePassword(password)
        return False

    def generateToken(self, username):
        """
        为用户生成令牌。

        参数:
            username (str): 要为其生成令牌的用户名。

        返回:
            str: 生成的令牌，如果用户不存在，则为None。
        """
        for user in self.userList:
            if user.username == username:
                return user.randomToken()
        return None

    def validateToken(self, username, token):
        """
        验证用户的令牌。

        参数:
            username (str): 要验证令牌的用户名。
            token (str): 要验证的令牌。

        返回:
            bool: 如果令牌有效，则为True，否则为False。
        """
        for user in self.userList:
            if user.username == username:
                return user.checkToken(token)
        return False

    def getUserBox(self, username):
        """
        获取与用户关联的箱子。

        参数:
            username (str): 要获取箱子的用户名。

        返回:
            Box: 与用户关联的箱子，如果用户不存在，则为None。
        """
        for user in self.userList:
            if user.username == username:
                for box in self.boxesList:
                    if box.id == user.boxID:
                        return box
        return None

    def refreshAllImage(self):
        """
        刷新所有箱子的图像。
        """
        for box in self.boxesList:
            box.refreshImage()


class Box:
    """
    Box类表示系统中的一个箱子。

    属性:
        id (int): 箱子的ID。
        tempSensor (str): 与箱子关联的温度传感器的ID。
        pump (str): 与箱子关联的泵的ID。
        camera (str): 与箱子关联的相机的ID。
    """

    def __init__(self, id, tempSensor=None, pump=None, camera=None):
        """
        使用给定的ID和可选的传感器、泵和相机ID初始化Box类。
        """
        self.id = id
        self.tempSensor = tempSensor
        self.pump = pump
        self.camera = camera

    def __str__(self):
        """
        返回箱子的JSON格式的字符串表示形式。
        """
        return {'id': self.id, 'tempSensor': self.tempSensor, 'pump': self.pump, 'camera': self.camera}

    def getTemp(self):
        """
        从箱子的温度传感器获取温度。

        返回:
            float: 温度，如果无法读取温度，则为字符串错误消息。
        """
        dht_handler = DHTemp.DHTHandler()
        temperature, humidity = dht_handler.read_dht_data(self.tempSensor)
        if temperature is not None:
            return temperature
        return "未能成功读取温度数据"

    def getHumidity(self):
        """
        从箱子的温度传感器获取湿度。

        返回:
            float: 湿度，如果无法读取湿度，则为字符串错误消息。
        """
        dht_handler = DHTemp.DHTHandler()
        temperature, humidity = dht_handler.read_dht_data(self.tempSensor)
        if humidity is not None:
            return humidity
        return "未能成功读取湿度数据"

    def refreshImage(self):
        """
        刷新箱子相机的图像。
        """
        cam_handler = camHandler.CameraHandler()
        cam_handler.capture_single(self.camera, self.id)

    def openPump(self):
        """
        打开箱子的泵。此方法尚未实现。
        """
        pass


class User:
    """
    User类表示系统中的一个用户。

    属性:
        username (str): 用户的用户名。
        password (str): 用户的密码。
        token (str): 用户的登录令牌。
        expireTime (float): 用户的登录令牌的过期时间。
        boxID (int): 与用户关联的箱子的ID。
        autoLogoutTime (int): 用户自动注销的时间（秒）。
    """

    def __init__(self, username, password, token=None, expireTime=None, boxID=None):
        """
        使用给定的用户名和密码以及可选的令牌、过期时间和箱子ID初始化User类。
        """
        self.username = username
        self.password = password
        self.token = token
        self.expireTime =  expireTime
        self.boxID = boxID

        # 自动登出时间(秒)
        self.autoLogoutTime = 3600

    def __str__(self):
        """
        返回用户的JSON格式的字符串表示形式。
        """
        return {'username': self.username, 'password': self.password, 'token': self.token}

    def validatePassword(self, input_password):
        """
        验证密码。

        参数:
            input_password (str): 要验证的密码。

        返回:
            bool: 如果密码有效，则为True，否则为False。
        """
        return self.password == input_password

    def randomToken(self):
        """
        为用户生成随机登录令牌。

        返回:
            str: 生成的令牌。
        """
        import random
        import string
        self.token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.expireTime = time.time() + self.autoLogoutTime
        return self.token

    def checkToken(self, token):
        """
        检查登录令牌。

        参数:
            token (str): 要检查的令牌。

        返回:
            bool: 如果令牌有效，则为True，否则为False。
        """
        if self.expireTime < time.time():
            return False
        return self.token == token