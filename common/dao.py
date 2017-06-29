import pymysql

class Dao(object):
    cursor = None
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '',
        'charset':'utf8mb4',
        'db':'transfermarkt',
        'autocommit': True,
        'cursorclass':pymysql.cursors.DictCursor
    }

    @staticmethod
    def init():
        conn = pymysql.connect(**Dao.config)
        Dao.cursor = conn.cursor()

    @staticmethod
    def createEternalTable():
        sql  = 'create table if not exists eternal_table ('
        sql += 'id varchar(5) not null,'
        sql += 'league varchar(4) not null,'
        sql += 'level tinyint,'
        sql += 'years smallint,'
        sql += 'first smallint,'
        sql += '`match` smallint,'
        sql += 'win smallint,'
        sql += 'draw smallint,'
        sql += 'loss smallint,'
        sql += 'point smallint,'
        sql += 'primary key (id, league)'
        sql += ')'
        Dao.cursor.execute(sql)

    def getClubCount(id):
        Dao.cursor.execute('select id from club where id = %s', id)
        return Dao.cursor.rowcount

    def getEternalTable(id):
        Dao.cursor.execute('select id from eternal_table where id = %s', id)
        return Dao.cursor.rowcount

    def insertClub(param):
        sql = 'insert into club (id, name, nation) values(%s, %s, %s)'
        Dao.cursor.execute(sql, param)

    def insertEternalTable(param):
        sql = 'insert into eternal_table values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        Dao.cursor.execute(sql, param)

    def updateEternalTable(param):
        sql = 'update eternal_table set league = %s, level = %s, years = %s, first = %s, `match` = %s, win = %s, draw = %s, loss = %s, point = %s where id = %s'
        Dao.cursor.execute(sql, param)