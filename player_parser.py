import datetime
import json
import re
import requests
import time
from dao import Dao
from lxml import html

DOMAIN = "https://www.transfermarkt.co.uk/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]
PROXIES = [
    {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    {'ip_port': '122.224.249.122:8088', 'user_pass': ''}
]
NOW_DATE = datetime.datetime.today().strftime('%Y%m%d')
club_set = {}
country_set = {}

def parse_player_data(player_id):
    url  = DOMAIN + "player/profil/spieler/" + str(player_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # name
    nameBlock = content.xpath('//div[@class="dataName"]/h1')[0]
    fullName = nameBlock.text_content()
    nameBlock = nameBlock.xpath('b')[0]
    name = nameBlock.text_content()

    # full name
    dataBlock = content.xpath('//table[@class="auflistung"]')[0]
    tempTH = dataBlock[0].xpath('th')[0].text_content()
    if tempTH == "Name in home country:" or tempTH == "Complete name:":
        fullName = dataBlock[0].xpath('td')[0].text_content().strip()

    # birthday
    birthday = content.xpath('//span[@itemprop="birthDate"]')[0].text_content()
    birthday = birthday.split('(')[0].strip().replace(',', '')
    tempTime = time.mktime(time.strptime(birthday, '%b %d %Y'))
    birthday = time.strftime("%Y%m%d", time.gmtime(tempTime))

    # nationality
    nationality = content.xpath('//span[@class="dataValue"]/a[@class="vereinprofil_tooltip"]')
    if len(nationality) > 0:
        nationality = nationality[0].attrib['id']
        if int(nationality) not in country_set:
            nationality = get_national_id(nationality)
    else:
        nationality = "0"

    # position
    positionBlock = content.xpath('//div[@class="large-5 columns infos small-12"]/div[@class="auflistung"]/div')
    position = get_position_id(positionBlock[0].text_content().split(':')[1].strip())

    # height
    height = content.xpath('//span[@itemprop="height"]')[0].text_content().strip()
    height = re.sub("\D", "", height)
    height = int(height)

    # build player data
    param = (
        player_id, 
        fullName, name, birthday, nationality, position, height, 0, NOW_DATE, 
        fullName, name, birthday, nationality, position, height, NOW_DATE, 
    )
    Dao.upsert_player(param)

    print(fullName + ", " + name + ", " + birthday + ", " + nationality)

    # parse_market_data(player_id, response.text)

def parse_market_data(player_id, response):

    marketData = response.split("'Marktwert','data':")[1]
    marketData = marketData.split("}],'legend'")[0]
    marketData = marketData.replace("'", '"')

    tempClub = ''
    for data in marketData:
        club = data['marker']['symbol']
        if club != 'circle':
            club = club.split('/tiny/')[1]
            club = club.split('.')[0].split('_')[0]
            tempClub = club
        else:
            club = tempClub
        marketValue = str(data['y'])
        recrodDate = data['datum_mw'].replace(',', '')
        tempTime = time.mktime(time.strptime(recrodDate, '%b %d %Y'))
        recrodDate = time.strftime("%Y%m%d", time.gmtime(tempTime))

        param = (
            player_id, 
            club, recrodDate, marketValue, NOW_DATE, 
            club, recrodDate, marketValue, NOW_DATE, 
        )
        Dao.upsert_market(param)
        print(club + ", " + marketValue + ", " + recrodDate)

def parse_performance_data(player_id):
    url  = DOMAIN + "player/detaillierteleistungsdaten/spieler/" + str(player_id) + "/plus/1"
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    dataBlock = content.xpath('//div[@id="yw1"]/table[@class="items"]/tbody/tr')
    for row in dataBlock:
        td = row.xpath('td')
        season = td[0].text_content()
        club = row.xpath('td[4]/a')[0].attrib['id']
        appearance = td[4].text_content().replace("-", "0")
        goal = td[5].text_content().replace("-", "0")
        if len(td) > 15:
            assist = td[6].text_content().replace("-", "0")
            yellow = td[10].text_content().replace("-", "0")
            red = td[12].text_content().replace("-", "0")
            minute = re.sub("\D", "", td[15].text_content().replace("-", "0"))
        else:
            assist = '0'
            yellow = td[9].text_content().replace("-", "0")
            red = td[11].text_content().replace("-", "0")
            minute = re.sub("\D", "", td[14].text_content().replace("-", "0"))

        if club in club_set:
            param = (
                player_id, 
                season, club, appearance, goal, assist, yellow, red, minute, 
                season, club, appearance, goal, assist, yellow, red, minute
            )
            Dao.upsert_career(param)
            print(season + ", " + club + ", " + appearance + ", " + goal + ", " + assist + ", " + yellow + ", " + red + ", " + minute)

def parse_national_team_data(player_id):
    url  = DOMAIN + "player/nationalmannschaft/spieler/" + str(player_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    dataBlock = content.xpath('//div[@class="large-8 columns"]/div[@class="box"][1]/table/tbody/tr')
    td = dataBlock[1].xpath('td')

    nationality = td[1].xpath('//span[@class="dataValue"]/a[@class="vereinprofil_tooltip"]')
    if (len(nationality)) > 0:
        nationality = nationality[0].attrib['id']

    if nationality in country_set:
        appearance = td[4].text_content().replace("-", "0")
        goal = td[5].text_content().replace("-", "0")
        debut_date = td[3].text_content().strip().replace(',', '')
        tempTime = time.mktime(time.strptime(debut_date, '%b %d %Y'))
        debut_date = time.strftime("%Y%m%d", time.gmtime(tempTime))
        debut_age = td[7].text_content().strip()

        param = (
            player_id, 
            nationality, appearance, goal, debut_date, debut_age, NOW_DATE, 
            nationality, appearance, goal, debut_date, debut_age, NOW_DATE
        )
        Dao.upsert_national_team(param)
        print(nationality + ", " + appearance + ", " + goal + ", " + debut_date + ", " + debut_age)

def build_club_set():
    result = Dao.get_all_club_id()
    global club_set
    club_set = { item['id'] for item in result }

def build_country_set():
    result = Dao.get_all_country_id()
    global country_set
    country_set = { item['id'] for item in result }

def get_position_id(position):
    return {
        'Keeper' : '1',
        'Left-Back' : '2',
        'Right-Back' : '3',
        'Sweeper' : '4',
        'Centre-Back' : '5',
        'Defensive Midfield' : '6',
        'Left Midfield' : '7',
        'Right Midfield' : '8',
        'Central Midfield' : '9',
        'Attacking Midfield' : '10',
        'Left Wing' : '11',
        'Right Wing' : '12',
        'Secondary Striker' : '13',
        'Centre-Forward': '14'
    }[position]

def get_national_id(nationality):
    return {
        '7658'  : '3439',   # BRAZIL U20
        '9323'  : '3377',   # FRANCE U21
        '3817'  : '3262',   # GERMANY U21
        '12609' : '3375',   # SPAIN U19
        '9567'  : '3375',   # SPAIN U21
        '16374' : '3300',   # PORTUGAL U21
        '22907' : '3299'    # ENGLAND U20
    }[nationality]

def get_all_player_by_team_id(team_id):
    url  = DOMAIN + "jumplist/startseite/verein/" + str(team_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    player_list = []
    link = content.xpath('//table[@class="inline-table"]//tr[1]/td[2]/div[1]/span/a')
    for i in link:
        player_list.append(int(i.attrib['id']))

    return player_list

"""
Main
"""
Dao.init()
Dao.create_player_table()
Dao.create_career_table()
Dao.create_nation_table()
Dao.create_market_table()

build_club_set()
build_country_set()

"""
team_id :
    281 = Manchester City,     985 = Manchester United
    148 = Tottenham Hotspur
"""
player_list = get_all_player_by_team_id(148)
print(player_list)

for player_id in player_list:
    parse_player_data(player_id)
    parse_performance_data(player_id)
    # parse_national_team_data(player_id)
    time.sleep(1)