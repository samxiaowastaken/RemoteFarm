from bottle import route, run, request, template, redirect, response

# 测试时保留的用户列表
userList = ["SamXiao"]
passwrList = ["2007"]

@route('/')
def home():
    # 检查是否设置了登录cookie
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in:
        # 已登录，重定向到 /view
        redirect('/view')
    else:
        # 未登录，返回包含表单的 HTML 页面
        return template(loginPage, name=None)

@route('/login', method='POST')
def login():
    # 获取表单输入
    username = request.forms.get('username')
    password = request.forms.get('password')
    # 验证登录逻辑
    if username in userList:
        if passwrList[userList.index(username)] == password:
            # 登录成功，设置cookie并重定向到 viewPage 路由
            response.set_cookie("is_logged_in", "yes", path="/")
            response.set_cookie("username", username, path="/")  # 设置用户名的cookie
            redirect('/view')
        else:
            return template(loginError, reason="用户所输入的密码错误，请检查后重试")
    else:
        return template(loginError, reason="用户 {} 不存在，请检查你的输入".format(username))

@route('/view')
def view_page():
    # 检查是否设置了登录cookie
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in:
        # 从cookie中获取用户名
        username = request.get_cookie("username")
        # 显示 viewPage.html 的内容，并传递用户名
        return template(viewPage, userName=username)
    else:
        # 未登录，重定向到首页
        redirect('/')

@route('/logout')
def logout():
    # 检查是否设置了登录cookie
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in:
        # 清空cookie来登出用户
        response.delete_cookie("is_logged_in", path="/")
        response.delete_cookie("username", path="/")
        # 重定向到登出成功页面
        redirect('/logoutSuccess')
    else:
        # 重定向到登出失败页面
        redirect('/logoutFailed')

if __name__ == '__main__':
    # 初始化读入模板内容
    # 登录页
    with open("loginPage.html", mode="r", encoding="UTF-8") as t:
        loginPage = t.read()
    # 登录错误页
    with open("loginError.html", mode="r", encoding="UTF-8") as t:
        loginError = t.read()
    # 登陆后主界面
    with open("viewPage.html", mode="r", encoding="UTF-8") as t:
        viewPage = t.read()
    # 登出成功页
    with open("logoutSuccess.html", mode="r", encoding="UTF-8") as t:
        logoutSuccess = t.read()
    # 登出失败页
    with open("logoutFailed.html", mode="r", encoding="UTF-8") as t:
        logoutFailed = t.read()

    run(host='localhost', port=8080, debug=True)