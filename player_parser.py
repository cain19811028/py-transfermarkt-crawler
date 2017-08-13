import datetime
import json
import re
import requests
import time
from common.dao import Dao
from lxml import html

DOMAIN = "https://www.transfermarkt.co.uk/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
CLUB_SET = {}
NOW_DATE = datetime.datetime.today().strftime('%Y%m%d')

def parsePlayerData(playerId):
    url  = DOMAIN + "player/profil/spieler/" + str(playerId)
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
    if tempTH == "Name in home country:" or "Complete name:":
        fullName = dataBlock[0].xpath('td')[0].text_content().strip()

    # birthday
    birthday = content.xpath('//span[@itemprop="birthDate"]')[0].text_content()
    birthday = birthday.split('(')[0].strip().replace(',', '')
    tempTime = time.mktime(time.strptime(birthday, '%b %d %Y'))
    birthday = time.strftime("%Y%m%d", time.gmtime(tempTime))

    # nationality
    nationality = content.xpath('//a[@class="vereinprofil_tooltip"]')[0].attrib['id']

    # position
    positionBlock = content.xpath('//div[@class="large-5 columns infos small-12"]/div[@class="auflistung"]/div')
    position = getPositionId(positionBlock[0].text_content().split(':')[1].strip())

    # height
    height = content.xpath('//span[@itemprop="height"]')[0].text_content().strip()
    height = re.sub("\D", "", height)

    # build player data
    count = Dao.getPlayerCount(playerId)
    if(count == 0):
        param = (playerId, fullName, name, '', birthday, nationality, position, height, 0, 0, NOW_DATE)
        Dao.insertPlayer(param)
    else:
        param = (fullName, name, nationality, position, height, NOW_DATE, playerId)
        Dao.updatePlayer(param)

    print(fullName + ", " + name + ", " + birthday + ", " + nationality + ", " + height + ", " + position)

    parseMarketData(playerId, response.text)

def parseMarketData(playerId, response):

    marketData = response.split("'Marktwert','data':")[1]
    marketData = marketData.split("}],'legend'")[0].replace("'", "\"")
    marketData = json.loads(marketData)
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

        count = Dao.getMarketCount(playerId, club, recrodDate)
        if(count == 0):
            param = (playerId, club, recrodDate, marketValue, NOW_DATE)
            Dao.insertMarket(param)
        else:
            param = (marketValue, NOW_DATE, playerId, club, recrodDate)
            Dao.updateMarket(param)

        print(club + ", " + marketValue + ", " + recrodDate)

def parsePerformanceData(playerId):
    url  = DOMAIN + "player/detaillierteleistungsdaten/spieler/" + str(playerId) + "/plus/1"
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


        if club in CLUB_SET:
            count = Dao.getCareerCount(playerId, season, club)
            if(count == 0):
                param = (playerId, season, club, appearance, goal, assist, yellow, red, minute)
                Dao.insertCareer(param)
            else:
                param = (appearance, goal, assist, yellow, red, minute, playerId, season, club)
                Dao.updateCareer(param)

        print(season + ", " + club + ", " + appearance + ", " + goal + ", " + assist + ", " + yellow + ", " + red + ", " + minute)

def parseNationalTeamData(playerId):
    url  = DOMAIN + "player/nationalmannschaft/spieler/" + str(playerId)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    dataBlock = content.xpath('//div[@class="large-8 columns"]/div[@class="box"][1]/table/tbody/tr')
    td = dataBlock[1].xpath('td')

    nationality = td[1].xpath('//a[@class="vereinprofil_tooltip"]')[0].attrib['id']
    appearance = td[4].text_content().replace("-", "0")
    goal = td[5].text_content().replace("-", "0")
    debut_date = td[3].text_content().strip().replace(',', '')
    tempTime = time.mktime(time.strptime(debut_date, '%b %d %Y'))
    debut_date = time.strftime("%Y%m%d", time.gmtime(tempTime))
    debut_age = td[7].text_content().strip()

    count = Dao.getNationalCount(playerId)
    if(count == 0):
        param = (playerId, nationality, appearance, goal, debut_date, debut_age, NOW_DATE)
        Dao.insertNationalTeam(param)
    else:
        param = (appearance, goal, debut_date, debut_age, NOW_DATE, playerId, nationality)
        Dao.updateNationalTeam(param)

    print(nationality + ", " + appearance + ", " + goal + ", " + debut_date + ", " + debut_age)

def buildClubSet():
    result = Dao.getAllClubId()
    global CLUB_SET
    CLUB_SET = { item['id'] for item in result }

def getPositionId(position):
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

"""
Main
"""
Dao.init()
Dao.createPlayerTable()
Dao.createCareerTable()
Dao.createNationTable()
Dao.createMarketTable()

playerId = 46741

buildClubSet()
parsePlayerData(playerId)
parsePerformanceData(playerId)
parseNationalTeamData(playerId)