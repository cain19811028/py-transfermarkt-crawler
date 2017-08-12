import datetime
import re
import requests
import time
from common.dao import Dao
from lxml import html

DOMAIN = "https://www.transfermarkt.co.uk/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

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
    if tempTH == "Name in home country:":
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
        param = (playerId, fullName, name, '', birthday, nationality, position, height, 0, datetime.datetime.today().strftime('%Y%m%d'))
        Dao.insertPlayer(param)
    else:
        param = (fullName, name, nationality, position, height, datetime.datetime.today().strftime('%Y%m%d'), playerId)
        Dao.updatePlayer(param)

    print(fullName + ", " + name + ", " + birthday + ", " + nationality + ", " + height + ", " + position)

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

playerId = 27511

parsePlayerData(playerId)