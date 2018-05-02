import pymysql

class Dao(object):
    cursor = None
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '',
        'charset':'utf8mb4',
        'db':'football',
        'autocommit': True,
        'cursorclass':pymysql.cursors.DictCursor
    }

    @staticmethod
    def init():
        conn = pymysql.connect(**Dao.config)
        Dao.cursor = conn.cursor()

    @staticmethod
    def create_eternal_table():
        sql = """
        create table if not exists eternal_table (
            id varchar(5) not null,
            league varchar(4) not null,
            level tinyint,
            years smallint,
            first smallint,
            appearance smallint,
            win smallint,
            draw smallint,
            loss smallint,
            goal smallint,
            point smallint,
            primary key (id, league)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def create_club_table():
        sql = """
        create table if not exists club (
            id varchar(5) not null,
            name varchar(40),
            nation smallint,
            founded varchar(4),
            ground varchar(50),
            capacity int,
            primary key (id)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def createPlayerTable():
        sql = """
        create table if not exists player (
            id varchar(10) not null,
            full_name varchar(40),
            name varchar(20),
            birthday varchar(8),
            nationality int,
            position tinyint,
            height int,
            retirement tinyint,
            modify_date datetime,
            primary key (id)
        ) 
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def createCareerTable():
        sql = """
        create table if not exists career (
            id varchar(10) not null,
            season varchar(5),
            club varchar(5),
            appearance tinyint,
            assist tinyint,
            yellow tinyint,
            red tinyint,
            minute smallint,
            primary key (id, season, club)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def createNationTable():
        sql = """
        create table if not exists national_team (
            id varchar(10) not null,
            nationality int,
            appearance tinyint,
            goal tinyint,
            debut_date varchar(8),
            debut_age varchar(30),
            modify_date datetime,
            primary key (id, nationality)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def createMarketTable():
        sql = """
        create table if not exists market (
            id varchar(10) not null,
            club varchar(5),
            record_date varchar(8),
            market_value bigint,
            modify_date datetime,
            primary key (id, club, record_date)
        )
        """
        Dao.cursor.execute(sql)

    @staticmethod
    def getAllClubId():
        Dao.cursor.execute('select distinct id from club')
        return Dao.cursor.fetchall()

    @staticmethod
    def getAllCountryId():
        Dao.cursor.execute('select distinct id from country')
        return Dao.cursor.fetchall()

    @staticmethod
    def getPlayerCount(id):
        Dao.cursor.execute('select id from player where id = %s', (id))
        return Dao.cursor.rowcount

    @staticmethod
    def getMarketCount(id, club, record_date):
        Dao.cursor.execute('select id from market where id = %s and club = %s and record_date = %s', (id, club, record_date))
        return Dao.cursor.rowcount

    @staticmethod
    def getCareerCount(id, season, club):
        Dao.cursor.execute('select id from career where id = %s and season = %s and club = %s', (id, season, club))
        return Dao.cursor.rowcount

    @staticmethod
    def getNationalCount(id):
        Dao.cursor.execute('select id from national_team where id = %s', (id))
        return Dao.cursor.rowcount

    @staticmethod
    def get_incomplete_club():
        sql = """
        select id from club 
        where founded is null or ground is null or capacity is null
        """
        Dao.cursor.execute(sql)
        return Dao.cursor.fetchall()

    @staticmethod
    def upsert_club(param):
        sql = """
        insert into club (id, name, nation) values(%s, %s, %s) 
        on duplicate key update id = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_eternal_table(param):
        sql = """
        insert into eternal_table values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        on duplicate key update id = %s, league = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def update_club_extra_data(param):
        sql = """
        update club set founded = %s, ground = %s, capacity = %s where id = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def insertPlayer(param):
        sql = 'insert into player values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def insertMarket(param):
        sql = 'insert into market values(%s, %s, %s, %s, %s)'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def insertCareer(param):
        sql = 'insert into career values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def insertNationalTeam(param):
        sql = 'insert into national_team values(%s, %s, %s, %s, %s, %s, %s)'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def updatePlayer(param):
        sql = 'update player set nationality = %s, position = %s, height = %s, modify_date = %s where id = %s'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def updateMarket(param):
        sql = 'update market set market_value = %s, modify_date = %s where id = %s and club = %s and record_date = %s'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def updateCareer(param):
        sql = 'update career set appearance = %s, goal = %s, assist = %s, yellow = %s, red = %s, minute = %s where id = %s and season = %s and club = %s'
        Dao.cursor.execute(sql, param)

    @staticmethod
    def updateNationalTeam(param):
        sql = 'update national_team set appearance = %s, goal = %s, debut_date = %s, debut_age = %s, modify_date = %s where id = %s and nationality = %s'
        Dao.cursor.execute(sql, param)