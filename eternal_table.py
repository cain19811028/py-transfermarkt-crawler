import datetime
import json
import pymysql
import re
import requests
from common.dao import Dao
from lxml import html

DOMAIN = "https://www.transfermarkt.co.uk/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
LASTYEAR = int(datetime.datetime.today().strftime('%Y')) - 1
LEAGUE = {}
LEAGUE["England"]  = {"id":"ENG", "leagueName":"premier-league", "leagueSimplify":"GB1", "startYear":"1992"}
LEAGUE["Spain"]    = {"id":"SPA", "leagueName":"laliga", "leagueSimplify":"ES1", "startYear":"1928"}
LEAGUE["Germany"]  = {"id":"GER", "leagueName":"1-bundesliga", "leagueSimplify":"L1", "startYear":"1963"}
LEAGUE["Italy"]    = {"id":"ITA", "leagueName":"serie-a", "leagueSimplify":"IT1", "startYear":"1929"}
LEAGUE["France"]   = {"id":"FRA", "leagueName":"ligue-1", "leagueSimplify":"FR1", "startYear":"1980"}
LEAGUE["Portugal"] = {"id":"PRT", "leagueName":"liga-nos", "leagueSimplify":"PO1", "startYear":"1990"}
LEAGUE["Turkey"]   = {"id":"TUR", "leagueName":"super-lig", "leagueSimplify":"TR1", "startYear":"1990"}

def getEternalTable(data):
    url  = DOMAIN + data["leagueName"] + "/ewigeTabelle/wettbewerb/"
    url += data["leagueSimplify"] + "/saison_id_von/"
    url += data["startYear"] + "/saison_id_bis/" + str(LASTYEAR) + "/tabllenart/alle/plus/1"
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)
    table = content.xpath('//table[@class="items"]/tbody/tr')
    for row in table:
        td = row.xpath('td')
        id = str(row.xpath('td/a/@id')[0])
        name = td[2].text_content()
        league = data["leagueSimplify"]
        tempLeague = td[3].text_content().replace(".Liga", "")
        level = tempLeague if re.match(r"(\d+)", tempLeague) else "99"
        years = td[4].text_content().replace(".", "")
        first = td[5].text_content().replace(".", "")
        match = td[6].text_content().replace(".", "")
        win = td[7].text_content().replace(".", "")
        draw = td[8].text_content().replace(".", "")
        loss = td[9].text_content().replace(".", "")
        point = td[13].text_content().replace(".", "")

        # build club data
        count = Dao.getClubCount(id)
        if(count == 0):
            param = (id, name, data["id"])
            Dao.insertClub(param)
            print(id + " : " + name + " : " + data["id"])

        # build eternal table
        count = Dao.getEternalTable(id)
        if(count == 0):
            param = (id, league, level, years, first, match, win, draw, loss, point)
            Dao.insertEternalTable(param)
        else:
            param = (league, level, years, first, match, win, draw, loss, point, id)
            Dao.updateEternalTable(param)

        print(id + " : " + name + " : " + league + " : " + level + " : " + years + " : " + first + " : " + match + " : " + win + " : " + draw + " : " + loss + " : " + point)

"""
Main
"""
Dao.init()
Dao.createEternalTable()
Dao.createClubTable()

for country in LEAGUE:
    getEternalTable(LEAGUE[country])