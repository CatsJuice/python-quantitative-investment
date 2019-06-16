import pymysql
import json

class DbManage(object):

    def __init__(self):
        f = open("const.json", "r", encoding='utf8')
        consts = json.loads(f.read())
        self.host = consts['mysql']['host']
        self.port = consts['mysql']['port']
        self.name = consts['mysql']['username']
        self.password = consts['mysql']['password']
        self.conn = None
        f.close()
    
    def connext(self):
        self.conn = pymysql.connect(self.host, self.name, self.password, charset='utf8')

    def executeSql(self, sqlTxt):
        cursor = self.conn.cursor()
        res = cursor.execute(sqlTxt)
        cursor.close
        return res

    def close(self):
        self.conn.close()