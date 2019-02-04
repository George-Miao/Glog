from flask import *
import pymysql, datetime, json, time


app = Flask(__name__)

# 函数定义
def ftime(a):
    if a.days == 0:
        if a.seconds // 3600 == 0:
            return f"{(a.seconds % 3600) // 60} 分钟前"
        else:
            return f"{a.seconds // 3600} 小时前"
    else:
        return f"{a.days} 天前"


def bid(limit=False):
    try:
        cursor.execute("select count(*) from block;")
        a = cursor.fetchone()
        db.commit()
        if a[0] > 10 and limit:
            bid = 10
        else:
            bid = a[0]
        return bid
    except:
        db.rollback()
        print("<------Bid Error------>")


def uid():
    try:
        cursor.execute("select count(*) from user;")
        a = cursor.fetchone()
        return a[0]
    except:
        db.rollback()
        print("<------Uid Error------>")


def generate(number):
    content = dict()
    try:
        cursor.execute(f"select * from block order by id desc limit {number};")
        results = cursor.fetchall()
        db.commit()
        for i in range(number):
            content[i] = {
                "id": results[i][0],
                "title": results[i][1],
                "post_time": ftime(datetime.datetime.now() - results[i][2]),
                "edit_time": ftime(datetime.datetime.now() - results[i][3]),
                "content": results[i][4]
            }
        return content
    except:
        db.rollback()
        print("<------Generate Error------>")


def specify(bid):
    try:
        cursor.execute(f"select * from block where id = {bid};")
        results = cursor.fetchall()
        content = {
            "id": f"a{results[0][0]}",
            "title": results[0][1],
            "content": results[0][4]
        }
        return content
    except:
        db.rollback()
        print("<------Specify Error------>")


def create(topic, content):
    try:
        number = bid() + 1
        cursor.execute(
            f"insert into block values('{number}', '{topic}', '{datetime.datetime.now()}', '{datetime.datetime.now()}', '{content}');"
        )
        db.commit()
        return number
    except:
        db.rollback()
        print("<------Create Error------>")


def edit(dict):
    try:
        if dict['id'] == "null":
            return "2"
        else:
            cursor.execute(f'''UPDATE block SET title = "{dict['title']}", content = "{dict['content']}", edit_time = "{dict['edit_time']}" where id = {int(dict['id'][1:])};''')
            db.commit()
            return "1"
    except:
        db.rollback()
        print("<------Edit Error------>")
    

def delete(bid):
    try:
        cursor.execute(f'''DELETE FROM block where id = {int(bid[1:])};''')
        db.commit()
    except:
        db.rollback()
        print("<------Delete Error------>")


def login(username, password):
    try:
        cursor.execute(f'''select user_id from user where username = "{username}" limit 1;''')
        a = cursor.fetchall()
        if a == ():
            return("000")
        else:
            a = a[0][0]
            cursor.execute(f'''select password from user where user_id = {a} limit 1;''')
            db_password = cursor.fetchone()
            if db_password[0] == password:
                cursor.execute(f'''UPDATE user SET last_login_time = "{datetime.datetime.now()}" where user_id = {a};''')
                db.commit()
                return ("001")
            else:
                return ("002")
    except:
        print ("<----login failed---->")
        

def check_login_status():
    username = request.cookies.get('username')
    if username == None:
        return "0"
    else:
        return username


def register(username, password):
    try:
        cursor.execute(f'''select user_id from user where username = "{username}" limit 1;''')
        a = cursor.fetchall()
        if a == ():
            user_id = uid() + 1
            cursor.execute(f'''insert into user values('{user_id}', '{username}', '{password}','{datetime.datetime.now()}', '{datetime.datetime.now()}')''')
            db.commit()
            return "000"
        else:
            return "001"
    except:
        print ("<----Register failed---->")
        
# 连接数据库
db = pymysql.connect("localhost", "root", "George219@", "mydb")


# 申明cursor
global cursor
cursor = db.cursor()


@app.route('/')
def home():
    username = check_login_status()
    number = bid(limit=True)
    content = generate(number)
    return render_template('content.html', username = username, number = number, title="Home", content=content)


@app.route('/me')
def me():
    username = check_login_status()
    return render_template('me.html', username = username, title="About Me")


@app.route("/editor")
def editor():
    number = bid()
    content = generate(number)
    return render_template("Editor.html", title="editor", number=number,  content=content)


@app.route("/login")
def login_page():
    username = check_login_status()
    if username != "0":
        return redirect("/")
    else:
        return render_template("user_handling/login.html", title = "Login")


@app.route("/register")
def Register_page():
    content = {
        "type": "Register"
    }
    return render_template("user_handling/register.html", title = "Register",**content)


@app.route("/user/<name>")
def userpage(name):
    username = check_login_status()
    if username == name:
        return f"own_userPage. Welcome back, {name}"
    else:
        if username == "0":
            return f"userpage. Welcome, guest"
        else:
            return f"userpage. Welcome, {username}"


@app.route("/login_handling", methods = ['GET', 'POST'])
def login_handling():
    name, passwd = request.form["username"], request.form["password"]
    a = login(name, passwd)
    if a == "001":
        a = make_response(a)
        a.set_cookie('username', name)
    return a

@app.route("/register_handling", methods = ['GET', 'POST'])
def register_handling():
    name, passwd = request.form["username"], request.form["password"]
    a = register(name, passwd)
    a = make_response(a)
    return a


@app.route("/save", methods=['GET', 'POST'])
def save():
    content = request.form.to_dict()
    content["edit_time"] = datetime.datetime.now()
    result = edit(content)
    return result
    

@app.route("/create", methods=['GET', 'POST'])
def new():
    bid = create("New blog", "")
    return f"a{bid}"


@app.route("/fetch", methods=['GET', 'POST'])
def fetch():
    bid = request.form["id"]
    bid = int(bid[1:])
    results = specify(bid)
    return json.dumps(results)


@app.route("/delete", methods=['GET', 'POST'])
def d():
    bid = request.form["id"]
    delete(bid)
    return "1"


@app.errorhandler(404)
def e_404(e):
    return render_template("error.html", title="404")


@app.errorhandler(500)
def e_500(e):
    return render_template("error.html", title="500")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = 1)
    cursor.close()
