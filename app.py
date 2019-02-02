from flask import *
import pymysql, datetime, json

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
        if a[0] > 10 and limit == 1:
            bid = 10
        else:
            bid = a[0]
        return bid
    except:
        db.rollback()
        print("<------Bid Error------>")


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


# 连接数据库
db = pymysql.connect("localhost", "root", "George219@", "mydb")


# 申明cursor
global cursor
cursor = db.cursor()


@app.route('/')
def home():
    number = bid(limit=True)
    content = generate(number)
    return render_template('content.html', number=number, title="Home", content=content)


@app.route('/me')
def me():
    return render_template('me.html', title="About Me")


@app.route("/500")
def r_500():
    return render_template("error.html", title="500")


@app.route("/editor")
def editor():
    number = bid()
    content = generate(number)
    return render_template("Editor.html", title="editor", number=number,  content=content)


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
    app.run(host="0.0.0.0", port=80)
    cursor.close()
