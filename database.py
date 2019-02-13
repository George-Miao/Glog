import pymysql
import datetime
import json


class Database(object):
    def connect(self, password, address = "localhost", user = "root", database = "mydb"):
        try:
            self.db = pymysql.connect(address, user, password, database)
            self.cursor = db.cursor()
        except:
            print("<---Connect error--->")

    def count(self, table):
        try:
            self.cursor.execute()
            number = self.cursor.fetchone()[0]
        except:
            print("<---Count error--->")

    def get_user_id(self, user_name):
        try:
            self.cursor.execute()
            number = self.cursor.fetchone([0])
        except:
            print("<---get user id error--->")

    def get_user_info(self, user_id):
        try:
            self.cursor.execute()
        except:
            print("<---get user info error--->")

    def get_block_content(self, block_id):
        try:
            self.cursor.execute()
        except:
            print("<---get block content error--->")

    def edit_block_content(self, block_id, content):
        try:
            self.cursor.execute()
        except:
            print("<---edit block content error--->")

    def delete_block(self, block_id):
        try:
            self.cursor.execute()
        except:
            print("<---delete block error--->")
    
    def create_block(self, title, content):
        try:
            self.cursor.execute()
        except:
            print("<---create block error--->")
        