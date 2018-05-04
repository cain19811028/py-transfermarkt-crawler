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
    def create_player_table():
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
    def create_career_table():
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
    def create_nation_table():
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
    def create_market_table():
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
    def get_all_club_id():
        sql = """
        select distinct id from club
        """
        Dao.cursor.execute(sql)
        return Dao.cursor.fetchall()

    @staticmethod
    def get_all_country_id():
        sql = """
        select distinct id from country
        """
        Dao.cursor.execute(sql)
        return Dao.cursor.fetchall()

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
    def update_club_extra_data(param):
        sql = """
        update club set founded = %s, ground = %s, capacity = %s where id = %s
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
    def upsert_player(param):
        sql = """
        insert into player values(%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        on duplicate key update id = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_market(param):
        sql = """
        insert into market values(%s, %s, %s, %s, %s)
        on duplicate key update id = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_career(param):
        sql = """
        insert into career values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        on duplicate key update id = %s
        """
        Dao.cursor.execute(sql, param)

    @staticmethod
    def upsert_national_team(param):
        sql = """
        insert into national_team values(%s, %s, %s, %s, %s, %s, %s)
        on duplicate key update id = %s
        """
        Dao.cursor.execute(sql, param)