from bottle import route, run, request, template, redirect, response,static_file
import dataHandler

# Initialize the data handler object
Boxes = dataHandler.Boxes()

# Read the HTML templates for various pages
with open("loginPage.html", mode="r", encoding="UTF-8") as t:
    loginPage = t.read()
with open("loginError.html", mode="r", encoding="UTF-8") as t:
    loginError = t.read()
with open("viewPage.html", mode="r", encoding="UTF-8") as t:
    viewPage = t.read()
with open("logoutSuccess.html", mode="r", encoding="UTF-8") as t:
    logoutSuccess = t.read()
with open("logoutFailed.html", mode="r", encoding="UTF-8") as t:
    logoutFailed = t.read()

@route('/',method='POST')
@route('/',method='GET')
def home():
    """
    Home route that checks if the user is logged in.
    If logged in, it redirects to the view page.
    If not, it returns the login page.
    """
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in:
        redirect('/view')
    else:
        return template(loginPage, name=None)

@route('/login', method='POST')
@route('/login', method='GET')
def login():
    """
    Login route that validates the user credentials.
    If valid, it sets the login cookies and redirects to the view page.
    If not, it returns the login error page.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    if Boxes.validateUser(username, password):
        response.set_cookie("is_logged_in", "yes", path="/")
        response.set_cookie("username", username, path="/")
        response.set_cookie("token", Boxes.generateToken(username), path="/")
        redirect('/view')
    else:
        return template(loginError, reason="用户所输入的密码错误，请检查后重试")

@route('/view', method='POST')
@route('/view', method='GET')
def view_page():
    """
    View page route that checks if the user is logged in.
    If logged in, it validates the token and returns the view page.
    If not, it redirects to the home page.
    """
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in== "yes":
        username = request.get_cookie("username")
        token = request.get_cookie("token")
        if not Boxes.validateToken(username, token):
            response.delete_cookie("is_logged_in", path="/")
            response.delete_cookie("username", path="/")
            response.delete_cookie("token", path="/")
            return template(loginError, reason="用户登录过期，请重新登录")
        return template(viewPage, userName=username, box_id=Boxes.getUserBox(username).id, humidity=Boxes.getUserBox(username).getHumidity(), temperature=Boxes.getUserBox(username).getTemp(), imageName="full_img.jpg")
    else:
        redirect('/')

@route('/logout', method='POST')
@route('/logout', method='GET')
def logout():
    """
    Logout route that checks if the user is logged in.
    If logged in, it deletes the login cookies and returns the logout success page.
    If not, it returns the logout failed page.
    """
    is_logged_in = request.get_cookie("is_logged_in")
    if is_logged_in:
        response.delete_cookie("is_logged_in", path="/")
        response.delete_cookie("username", path="/")
        response.delete_cookie("token", path="/")
        return template(logoutSuccess)
    else:
        return template(logoutFailed)

@route('/pics/<box_id>/<image_name>', method='GET')
def get_image(box_id, image_name):
    print(f"Getting image {image_name} from box {box_id}")
    """
    Route to get the image of the specified box.
    """
    return static_file(image_name, root=f"./data/pics/{box_id}/")

@route('/endpoint', method='POST')
def handle_command():
    """
    Endpoint route that handles commands sent from the web client.
    It performs actions based on the command received.
    """
    import json
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    data = request.json
    command = data['command']
    if command=='refreshPic':
        Boxes.getUserBox(username).refreshImage()
    elif command=='water':
        Boxes.getUserBox(username).openPump()
    return json.dumps({'status': 'success'})

if __name__ == '__main__':
    # Run the application
    run(host='localhost', port=8080, debug=True)