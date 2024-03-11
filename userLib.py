import random


class user:
    def __init__(self, username="默认用户", pwd="", boxid=None):
        self.username = username
        self.pwd = pwd
        # 箱子号
        self.boxid = boxid
        # 登录验证token，防止通过cookie登录
        self.loginToken = random.randint(10000, 99999)

    def loginAuth(self, pwdProvided):
        """
        登录操作，比对密码并且更换用户登录token
        :param pwdProvided:
        用户所提供的登录密码
        :return:
        比对成功时返回登录token，失败时返回False
        """
        if pwdProvided == self.pwd:
            self.loginToken = random.randint(10000, 99999)
            return self.loginToken
        else:
            return False

    def logout(self):
        """
        登出重置用户登录token，保证安全
        :return:
        始终返回True
        """
        self.loginToken = random.randint(10000, 99999)
