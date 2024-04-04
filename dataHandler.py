import time
import DHTemp
import camHandler

class Boxes:
    # 这里修改各种文件的读取/保存路径
    def __init__(self):
        self.boxConfigPath = './data/boxConfig.json'
        # 箱子文件保存路径

        self.imagePath = './data/image/'
        # 照片保存路径（如果是空目录，则按照箱子编号自动创建文件夹）

        self.userConfigPath = './data/userConfig.json'
        # 用户配置文件保存路径

        self.boxesList = []
        self.userList = []

        self.importBoxFromJson()
        self.importUserFromJson()

    # 从文件加载箱子配置
    def importBoxFromJson(self):
        import json
        with open(self.boxConfigPath, 'r') as file:
            data = json.load(file)
        for box in data:
            self.boxesList.append(Box(box['id'], box['tempSensor'], box['pump'], box['camera']))


    # 保存箱子配置到配置文件
    def saveBoxToJson(self):
        import json
        data = []
        for box in self.boxesList:
            data.append(str(box))
        with open(self.boxConfigPath, 'w') as file:
            json.dump(data, file)

    # 从文件加载用户配置
    def importUserFromJson(self):
        import json
        with open(self.userConfigPath, 'r') as file:
            data = json.load(file)
        for user in data:
            self.userList.append(User(user['username'], user['password'], user['token'], user['expireTime'], user['boxID']))

    # 验证用户登录
    def validateUser(self, username, password):
        for user in self.userList:
            if user.username == username:
                return user.validatePassword(password)
        return False

    # 生成用户token
    def generateToken(self, username):
        for user in self.userList:
            if user.username == username:
                return user.randomToken()
        return None

    # 验证登录token
    def validateToken(self, username, token):
        for user in self.userList:
            if user.username == username:
                return user.checkToken(token)
        return False

    # 返回对应用户的箱子
    def getUserBox(self, username):
        for user in self.userList:
            if user.username == username:
                for box in self.boxesList:
                    if box.id == user.boxID:
                        return box
        return None

    # 刷新所有箱子的照片
    def refreshAllImage(self):
        for box in self.boxesList:
            box.refreshImage()


class Box:
    # 初始化箱子
    def __init__(self, id, tempSensor=None, pump=None, camera=None):
        self.id = id
        self.tempSensor = tempSensor
        self.pump = pump
        self.camera = camera

    # 以json格式返回箱子信息
    def __str__(self):
        return {'id': self.id, 'tempSensor': self.tempSensor, 'pump': self.pump, 'camera': self.camera}

    # 获取箱子温度
    def getTemp(self):
        dht_handler = DHTemp.DHTHandler()
        temperature, humidity = dht_handler.read_dht_data(self.tempSensor)
        if temperature is not None:
            return temperature
        return "未能成功读取温度数据"
        # return 0

    # 获取箱子湿度
    def getHumidity(self):
        dht_handler = DHTemp.DHTHandler()
        temperature, humidity = dht_handler.read_dht_data(self.tempSensor)
        if humidity is not None:
            return humidity
        return "未能成功读取湿度数据"
        # return 0

    # 获取箱子照片
    def refreshImage(self):
        cam_handler = camHandler.CameraHandler()
        cam_handler.capture_single(self.camera, self.id)

    def openPump(self):
        # 这里还没写
        pass


class User:
    # 初始化用户
    def __init__(self, username, password, token=None, expireTime=None, boxID=None):
        self.username = username
        self.password = password
        self.token = token
        self.expireTime =  expireTime
        self.boxID = boxID

        # 自动登出时间(秒)
        self.autoLogoutTime = 3600

    # 以json格式返回用户信息
    def __str__(self):
        return {'username': self.username, 'password': self.password, 'token': self.token}

    # 验证密码
    def validatePassword(self, input_password):
        return self.password == input_password

    # 生成随机token
    def randomToken(self):
        import random
        import string
        self.token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.expireTime = time.time() + self.autoLogoutTime
        return self.token

    # 验证token
    def checkToken(self, token):
        if self.expireTime < time.time():
            return False
        return self.token == token

