import pymysql
import datetime
import json
from .methods import ftime
from flask import request
from flask import make_response
from flask import redirect


class Database(object):
    """和数据库的交互"""

    def connect(self, db=pymysql.connect("localhost", "root", "George219@", "mydb")):
        self.db = db
        self.cursor = db.cursor()

    # User
    def register(self, username, password):
        try:
            self.cursor.execute(
                f'''select user_id from user where username = "{username}" limit 1;''')
            exist_id = self.cursor.fetchall()
            if exist_id == ():
                user_id = self.get_user_id() + 1
                self.cursor.execute(
                    f'''insert into user values('{user_id}', '{username}', '{password}','{datetime.datetime.now()}', '{datetime.datetime.now()}')''')
                self.db.commit()
                return "000"
            else:
                return "001"
        except Exception as e:
            self.db.rollback()
            print(e)

    def login(self, username, password):
        try:
            self.cursor.execute(
                f'''select user_id from user where username = "{username}" limit 1;''')
            a = self.cursor.fetchall()
            if a == ():
                return("000")
            else:
                a = a[0][0]
                self.cursor.execute(
                    f'''select password from user where user_id = {a} limit 1;''')
                db_password = self.cursor.fetchone()
                if db_password[0] == password:
                    self.cursor.execute(
                        f'''UPDATE user SET last_login_time = "{datetime.datetime.now()}" where user_id = {a};''')
                    self.db.commit()
                    return ("001")
                else:
                    return ("002")
        except Exception:
            print("<------Login Error------>")
    
    # Content
    def get_block_id(self, is_limited=False):
        try:
            self.cursor.execute("select count(*) from block2;")
            a = self.cursor.fetchone()
            if a[0] > 10 and is_limited:  # 同一页最多显示十个内容block
                block_id = 10
            else:
                block_id = a[0]
            return block_id
        except:
            self.db.rollback()
            print("<------get_block_id Error------>")

    def get_user_id(self):
        try:
            self.cursor.execute("select count(*) from user;")
            user_info = self.cursor.fetchone()
            return user_info[0]
        except:
            self.db.rollback()
            print("<------Uid Error------>")

    def generate_content(self, number, is_detailed = False):
        content = dict()
        if not is_detailed:
            try:
                self.cursor.execute(f"select * from block2 order by id desc limit {number};")
                results = self.cursor.fetchall()
                for i in range(number):
                    content[i] = {
                        "id": results[i][0],
                        "title": results[i][1],
                        "content": results[i][2],
                        "post_time": ftime(datetime.datetime.now() - results[i][3]),
                        "edit_time": ftime(datetime.datetime.now() - results[i][4]),
                    }
                return content
            except:
                print("<------Undetailed Generate Error------>")
        else:
            try:
                self.cursor.execute(f"select * from block2 where id = {number};")
                results = self.cursor.fetchall()
                if results == ():
                    return "000"  #Does not exist
                else:
                    content = {
                        "id": results[0],
                        "title": results[1],
                        "content": results[2],
                        "post_time": ftime(datetime.datetime.now() - results[3]),
                        "edit_time": ftime(datetime.datetime.now() - results[4]),
                    }
                    return content
            except:
                print("<------Detailed Generate Error------>")

    # Editor
    def select(self, block_id):
        try:
            self.cursor.execute(f"select * from block2 where id = {block_id};")
            results = self.cursor.fetchall()
            content = {
                "id": f"a{results[0][0]}",
                "title": results[0][1],
                "content": results[0][2]
            }
            return content
        except:
            self.db.rollback()
            print("<------Specify Error------>")

    def create(self, title, content):
        try:
            number = self.get_block_id() + 1
            self.cursor.execute(
                f"insert into block2 values('{number}', '{title}', '{content}','{datetime.datetime.now()}', '{datetime.datetime.now()}'');"
            )
            self.db.commit()
            return number
        except:
            self.db.rollback()
            print("<------Create Error------>")

    def edit(self, block):
        try:
            if block['id'] == "null":
                return "2"
            else:
                self.cursor.execute(f'''UPDATE block2 SET title = "{block['title']}", 
                                            content = "{block['content']}", 
                                            edit_time = "{block['edit_time']}" where id = {int(block['id'][1:])};''')
                self.db.commit()
                return "1"
        except:
            self.db.rollback()
            print("<------Edit Error------>")

    def delete(self, block_id):
        try:
            self.cursor.execute(
                f'''DELETE FROM block2 where id = {int(block_id[1:])};''')
            self.db.commit()
        except:
            self.db.rollback()
            print("<------Delete Error------>")

    # Disconnect
    def disconnect(self):
        self.cursor.close()
