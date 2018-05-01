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

# European
LEAGUE["England"]     = {"id":"3299", "leagueName":"premier-league", "leagueSimplify":"GB1", "startYear":"1992"}
# LEAGUE["Spain"]       = {"id":"3375", "leagueName":"laliga", "leagueSimplify":"ES1", "startYear":"1928"}
# LEAGUE["Germany"]     = {"id":"3262", "leagueName":"1-bundesliga", "leagueSimplify":"L1", "startYear":"1963"}
# LEAGUE["Italy"]       = {"id":"3376", "leagueName":"serie-a", "leagueSimplify":"IT1", "startYear":"1929"}
# LEAGUE["France"]      = {"id":"3377", "leagueName":"ligue-1", "leagueSimplify":"FR1", "startYear":"1980"}
# LEAGUE["Portugal"]    = {"id":"3300", "leagueName":"liga-nos", "leagueSimplify":"PO1", "startYear":"1990"}
# LEAGUE["Turkey"]      = {"id":"3381", "leagueName":"super-lig", "leagueSimplify":"TR1", "startYear":"1990"}
# LEAGUE["Russia"]      = {"id":"3448", "leagueName":"premier-liga", "leagueSimplify":"RU1", "startYear":"1992"}
# LEAGUE["Netherlands"] = {"id":"3379", "leagueName":"eredivisie", "leagueSimplify":"NL1", "startYear":"1954"}
# LEAGUE["Belgium"]     = {"id":"3382", "leagueName":"jupiler-pro-league", "leagueSimplify":"BE1", "startYear":"2000"}
# LEAGUE["Greece"]      = {"id":"3378", "leagueName":"super-league", "leagueSimplify":"GR1", "startYear":"1988"}

# America
# LEAGUE["Brazil"]      = {"id":"3439", "leagueName":"campeonato-brasileiro-serie-a", "leagueSimplify":"BRA1", "startYear":"2005"}
# LEAGUE["Argentina"]   = {"id":"3437", "leagueName":"primera-division", "leagueSimplify":"AR1N", "startYear":"2014"}
# LEAGUE["Mexico"]      = {"id":"6303", "leagueName":"liga-mx-clausura", "leagueSimplify":"MEX1", "startYear":"2006"}
# LEAGUE["Mexico"]      = {"id":"6303", "leagueName":"liga-mx-apertura", "leagueSimplify":"MEXA", "startYear":"2006"}
# LEAGUE["America"]     = {"id":"3505", "leagueName":"major-league-soccer", "leagueSimplify":"MLS1", "startYear":"1995"}

# Asia
# LEAGUE["China"]       = {"id":"5598", "leagueName":"chinese-super-league", "leagueSimplify":"CSL", "startYear":"1993"}
# LEAGUE["Japan"]       = {"id":"3435", "leagueName":"j1-league", "leagueSimplify":"JAP1", "startYear":"2004"}
# LEAGUE["Korea"]       = {"id":"3589", "leagueName":"k-league-classic", "leagueSimplify":"RSK1", "startYear":"2009"}

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
        goal = td[10].text_content().split(":")[0].replace(".", "")
        point = td[13].text_content().replace(".", "")

        # build club data
        count = Dao.getClubCount(id)
        if(count == 0):
            param = (id, name, data["id"])
            Dao.insertClub(param)
            print(id + " : " + name + " : " + data["id"])

        # build eternal table
        count = Dao.getEternalTableCount(id, league)
        if(count == 0):
            param = (id, league, level, years, first, match, win, draw, loss, goal, point)
            Dao.insertEternalTable(param)
        else:
            param = (league, level, years, first, match, win, draw, loss, goal, point, id)
            Dao.updateEternalTable(param)

        print(id + " : " + name + " : " + league + " : " + level + " : " + years + " : " + first + " : " + match + " : " + win + " : " + draw + " : " + loss + " : " + goal + " : " + point)

def updateClubExtraData():
    result = Dao.getNotCompleteClub()
    for club in result:
        foundation = ""
        stadium = ""
        seat = 0

        url  = DOMAIN + "club/datenfakten/verein/" + club["id"]
        response = requests.get(url, headers = HEADERS)
        content = html.fromstring(response.text)

        # get stadium and seat data
        span = content.xpath('//div[@class="dataDaten"][2]/p[2]/span[2]')
        if len(span[0].xpath('a')) > 0:
            stadium = span[0].xpath('a')[0].text_content()
            seat = span[0].xpath('span')[0].text_content().replace(" Seats", "").replace(".", "")

        # get foundation data
        table = content.xpath('//table[@class="profilheader"]/tr')
        for row in table:
            th = row.xpath('th')[0].text_content()
            td = row.xpath('td')[0].text_content()
            if th == "Foundation:":
                if td.find(",") > -1:
                    foundation = td.split(',')[1].strip()

        param = (foundation, stadium, seat, club["id"])
        Dao.updateClubExtraData(param)
        print(club["id"] + ", " + foundation + ", " + stadium + ", " + str(seat))

"""
Main
"""
Dao.init()
Dao.createEternalTable()
Dao.createClubTable()

for country in LEAGUE:
    getEternalTable(LEAGUE[country])

updateClubExtraData()