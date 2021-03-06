"""
BY KEVIN WANG
THIS PROGRAM CONTAINS A VARIETY OF FUNCTIONS TO RETRIEVE DATA FROM VALVE'S DOTA 2 API
AND CALCULATE WINRATES AND OTHER STATISTICS FROM THAT DATA
"""
#MASKOFMADNESS.COM
#GGBRANCH.COM
#DAGON5.COM
#to do: more than 250 matches, and exclude diretide
#specify timeframe for winrates etc. maybe retrieve a timeframe of matchdetails
#add appending only the matches not already saved in saveAllMatches and saveAllDetails
#match details should probably be stored as ElementTrees, since they are never used in
#string form.
#pressing issue: make it better
# -appending new matches to a user's matchfiles should be appending, not rewriting.
# -speed in parsing details, such as item winrates.


#1. when getting match_ids from the api, start_at_match_id should be the most recent game saved already, to speed it up when those match_ids are fed into getMatchDetails
#2. when saving, append.  don't rewrite.

#idea for tearing this down and remaking: a hashmap to store matches where key = match_id: value = match_details
import requests
import os
import pickle
import xml.etree.ElementTree as ET
import json
import items
import time

mabufula = "40753485"
arthor = "47199737"
flameant = "29065860"
girlgamer = "128596275"
pro_players = {'Scandal': '86750262', 'Bulldong': '76482434', 'Waga': '32995405', 's4': '41231571'}

#os.chdir("Shackleshot") #This is for pythonanywhere

with open("config.txt", 'r') as f:
    apikey = f.read()

def getItems():
    try:
        #getting items from unofficial item schema http://www.dota2.com/jsfeed/itemdata
        itemjs = requests.get("http://www.dota2.com/jsfeed/itemdata").json()
        itemdict = {str(itemjs['itemdata'][i]['id']):i for i in itemjs['itemdata']}
        #print(itemdict)
        return itemdict
    except:
        #item schema didn't work
        print("DOTA 2 ONLINE ITEM SCHEMA NOT WORKING")
        return items.itemray

class ItemMap(dict):
    def __init__(self):
        dict.__init__(self, getItems())
    def __getitem__(self, arg):
        try:
            return dict.__getitem__(self,arg)
        except KeyError:
            return "recipe"

def getAllHeroes():
    herojs = requests.get("https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key={}&language=en_us".format(apikey)).json()
    herodict = {str(hero['id']): hero['localized_name'] for hero in herojs['result']['heroes']}
    return herodict

ITEMS = ItemMap()
HEROES = getAllHeroes()

def getAllMatches(playerid, end_match_id = ""):
    """returns the most recent 500 games by the player as a list of match_ids (strings) from the API."""
    #"You can "combine" filters.
    #i.e. account_id + hero_id = up to 500 matches per hero_id
    # so if you're not a player with 2874 Sand King games,
    #you should be easily able to fetch all your games with a couple API requests."
    #
    #^use this to get past the date_max removal
    matchlist = []
    matchnum=0
    sequence = 0
    maxmatch = ""
    prevmatch = '9999'
    #maxtime = 9999926270
    go = True
    
    while go == True:
        sequence+=1
        #maxtime = str(maxtime)
        #print("maxtime: " + maxtime)
        print("maxmatch: ", maxmatch)
        r = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?"
                         "format=%s"
                         "&key=%s"
                         "&account_id=%s"
                         "&matches_requested=%s"
                         "&start_at_match_id=%s"%("XML",apikey,playerid,"60",maxmatch))
        tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
        matches=tree.find("matches").findall("match")
        if not matches:
            break
        for h in matches:
            matchnum+=1
            #maxtime = h.findtext('start_time')
            #print(maxtime)
            maxmatch = h.find("match_id").text
            if maxmatch==end_match_id:
                go = False
                break
            #this is needed to recognize the last match
            #if maxmatch in matchlist:
            #    go = False
            if maxmatch == prevmatch:
                if double == True:
                    go = False
                double = True
            else:
                double = False
            prevmatch = maxmatch
            matchlist.append(maxmatch)
            print("match " + maxmatch)
        print('')
        time.sleep(1)
    print("matches: " + str(matchnum))
    print("sequence: " + str(sequence))
    matchlist = removeDuplicates(matchlist)
    print("non-duplicate matches: " + str(len(matchlist)))
    print("duplicate matches: " + str(matchnum-len(matchlist)))
    return matchlist

def getMostRecentSavedMatch(playerID):
    try:
        with open("matches" + str(playerID) + ".txt", "rb") as p:
            return pickle.load(p)[0]
    except:
        return ""

def saveAllMatches(playerID,overwrite = True):
    """saves match IDs from getAllMatches to a txt file. Returns the newly added matches"""
    try:
        with open("matches"+str(playerID)+".txt",'rb') as p:
            pass
    except IOError:
        allmatches = getAllMatches(playerID)
        with open("matches"+str(playerID)+".txt",'wb') as p:
            pickle.dump(allmatches,p)
        return allmatches
    else:
        mostrecent = getMostRecentSavedMatch(playerID)
        newmatches = getAllMatches(playerID, end_match_id = mostrecent)
        with open("matches"+str(playerID)+".txt",'rb') as p:
            prev = pickle.load(p)
            prev = newmatches + prev
            prev = removeDuplicates(prev)
        with open("matches"+str(playerID)+".txt",'wb') as p:
            pickle.dump(prev, p)
        return newmatches
        #if overwrite:
        #    allmatches = getAllMatches(playerID)
        #    with open("matches"+str(playerID)+".txt",'wb') as p:
        #        pickle.dump(allmatches,p)
        #else:
        #    pass

def getAllDetails(matchfile = None, match_ids = None):
    """given a file of match_ids OR a list of match_ids, return a list of match_details (as XML strings) from the API.
    If both parameters are given, the list will take precedence."""
    assert any((matchfile, match_ids)), "You must supply an argument."
    allDetailsXML = []
    if matchfile!=None:
        with open(matchfile, 'rb') as f:
            matchlist = pickle.load(f)
    else:
        matchlist = match_ids

    for i in matchlist:
        try:
            r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
                             "?format=%s"
                             "&key=%s"
                             "&match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",i))
        except:
            print("failed. " + i + ". Trying again.")
            try:
                r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
                                 "?format=%s"
                                 "&key=%s"
                                 "&match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",i))
            except:
                print("failed again.  skipping.")
        allDetailsXML.append(r.text)
        #print r.text
        print(i)
    return allDetailsXML

def saveDetails(alldetails, title, overwrite = True):
    "Given a list of match_details, save to a file."
    try:
        with open(title,'r') as q:
            #if this doesn't raise an error, then the file already exists
            print("FILE EXISTS")
            pass
    except IOError:
        #this probably means that the file doesn't exist yet.
        print("FILE DOESN'T EXIST YET.  WRITING.")
        with open(title,'wb') as p:
            pickle.dump(alldetails,p)
    else:
        #if the file already exists
        with open(title, 'rb') as p:
            prev = pickle.load(p)
            prev = alldetails + prev
            prev = removeDuplicates(prev)
        with open(title, 'wb') as p:
            pickle.dump(prev, p)
        #if overwrite:
        #    print("OVERWRITING")
        #    with open(title,'wb') as p:
        #        pickle.dump(alldetails,p)
        #else:
        #    print("NOT OVERWRITING")
        #    pass

#def saveAllDetails(playerID,overwrite = True):
#    """Given a playerID, get the details and save it using saveDetails"""
    #not used anywhere anymore now that saveAllDetailsFromID is refactored?
#    saveDetails(getAllDetails("matches"+str(playerID)+".txt"),
#                "matchdetails"+str(playerID)+".txt", overwrite)

def openDetails(playerID):
    with open("matchdetails"+str(playerID)+".txt", 'rb') as f:
        matchdetails = pickle.load(f) 
    return matchdetails

def saveAllDetailsFromID(playerID,overwrite = True):
    print("saving all matches")
    newmatches = saveAllMatches(playerID,overwrite)
    print("saving all details")
    saveDetails(getAllDetails(match_ids = newmatches), "matchdetails"+str(playerID)+".txt")

def saveAllDetailsFromIDs(*playerIDs, title = None, overwrite = True):
    """usage example: saveAllDetailsFromIDs(*pro_players.items(), 'pro_players')"""
    if title == None:
        if len(playerIDs) == 1:
            title = "matchdetails"+str(playerID)+".txt"
        else:
            raise TypeError("Title is required for multiple playerIDs")
    details = []
    for playerID in playerIDs:
        print("saving all matches: ", playerID)
        saveAllMatches(playerID,overwrite)
        print("getting all details: ", playerID)
        details.extend(getAllDetails("matches"+str(playerID)+".txt"))
    saveDetails(details, title, overwrite)

def findAllGamesWithItem(myID,item):
    #return a list of all match details with the item
    itemmatches = []
    itemmatchdetails = []
    amount = 0
    matchdetails = openDetails(myID)
    for match in matchdetails:
        try:
            tree = ET.fromstring(match.encode('ascii', 'ignore'))
            players =tree.find("players").findall("player")
            for player in players:
                if player.find("account_id").text == myID:
                    user = player
                    break
            for i in range(0,5):
                curitem = user.find("item_"+str(i))
                if curitem.text == str(item):
                    amount+=1
                    #print getHero(player.findtext("hero_id")) + " - " + tree.findtext("match_id")
                    itemmatches.append(tree.findtext("match_id"))
                    itemmatchdetails.append(match)
                    #print "http://dotabuff.com/matches/"+tree.findtext("match_id")
                    break
        except:
            print("user not found in game " + tree.findtext("match_id"))
    print(str(amount) + " games with "+ ITEMS[str(item)])
    return itemmatchdetails

def calculateWinrateFromDetails(myID, matchdetails):
    wins = 0
    for match in matchdetails:
        try:
            tree = ET.fromstring(match.encode('ascii', 'ignore'))
        except:
            print("could not parse match")
            continue
        try:
            players = tree.find("players").findall("player")
            for player in players:
                if player.find("account_id").text == myID:
                    if int(player.find('player_slot').text) < 5:
                        radiant = 'true'
                    else:
                        radiant = 'false'
                    break
        except:
            print("user not found")
        if radiant == tree.findtext('radiant_win'):
            wins+=1
    try:
        winpercent = round(float(100*wins)/len(matchdetails),1)
        print(str(wins) + "/" + str(len(matchdetails)) + " - " + str(winpercent) + "%")
    except ZeroDivisionError:
        #hey it's pythonic!
        winpercent = -1
        print("not found!")
    return (wins,len(matchdetails),winpercent)

def calculateWinrateItem(myID, item):
    return calculateWinrateFromDetails(myID,findAllGamesWithItem(myID,item))

def calculateWinrateForAllItems(myID):
    winrates = []
    iteration = 0
    for i in ITEMS:
        print(str(iteration) + " out of " + str(len(ITEMS)))
        iteration+=1
        winrates.append((i,calculateWinrateItem(myID,i)))
    sortList(winrates)
    print(winrates)
    for winrate in winrates:
        print(str(winrate[1][2]) + "%  - " + ITEMS[str(winrate[0])] + " - " + str(winrate[1][0]) + "/" + str(winrate[1][1]))

def getAllPlayedWith(myID,matchdetails=None, threshold = 2):
    if matchdetails is None:
        matchdetails = openDetails(myID)
    users = {}
    for match in matchdetails:
        try:
            tree = ET.fromstring(match.encode('ascii', 'ignore'))
        except:
            continue
        try:
            players = tree.find("players").findall("player")
            for player in players:
                playerid = player.find("account_id").text
                if playerid in users:
                    users[playerid]+=1
                else:
                    users[playerid]=1
        except:
            print("user not found")
    for user in sorted(users, key = lambda x: users[x]):
        if users[user] > threshold:
            r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
                             "format=%s"
                             "&key=%s"
                             "&steamids=%s"%("XML",apikey,int(user)+76561197960265728))
            tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
            player =tree.find("players").find("player")
            try:
                print(str(users[user]) + " - " + player.findtext('personaname') + " - " + str(user))
            except:
                print(str(users[user]) + " - " + user + " invalid.")
    return sorted([user for user in users if users[user] > threshold], key = lambda x: users[x])

def getPlayedWith(myID,friendID,matchdetails=None):
    #playermatches = []
    if matchdetails is None:
        matchdetails = openDetails(myID)
    playedwith = []
    playedagainst = []
    for match in matchdetails:
        inthegame = False
        try:
            tree = ET.fromstring(match.encode('ascii', 'ignore'))
        except:
            print("could not parse match")
            continue
        try:
            players = tree.find("players").findall("player")
            friendradiant = myradiant = None
            for player in players:
                playerid = player.find("account_id").text
                if playerid == friendID:
                    #playermatches.append(tree.findtext("match_id"))
                    if int(player.find('player_slot').text) < 5:
                        friendradiant = 1
                    else:
                        friendradiant = 0
                elif playerid == myID:
                    if int(player.find('player_slot').text) < 5:
                        myradiant = 1
                    else:
                        myradiant = 0
                if (friendradiant is not None) and (myradiant is not None):
                    inthegame = True
                    break
        except:
            print("error")
        if inthegame:
            if (friendradiant+myradiant)%2 == 0:
                print(tree.findtext("match_id") + " played with")
                playedwith.append(match)
            else:
                print(tree.findtext("match_id") + " played against")
                playedagainst.append(match)
    return (playedwith,playedagainst)

def calculateWinrateWith(myID,friendID):
    allplayedwith = getPlayedWith(myID,friendID)
    print("played with")
    calculateWinrateFromDetails(myID,allplayedwith[0])
    print("played against")
    calculateWinrateFromDetails(myID,allplayedwith[1])

def sortList(asdf):
    asdf.sort(key=lambda price: price[1][2])

def removeDuplicates(_list):
    newlist = []
    for i in _list:
        if i not in newlist:
            newlist.append(i)
    return newlist

def getHero(heroID):
    return HEROES[heroID]
    #with open("heroes.xml",'r') as r:
    #    tree = ET.fromstring(r.read().encode('ascii', 'ignore'))
    #    heroes = tree.find("heroes").findall("hero")
    #    for hero in heroes:
    #        if hero.findtext("id")==str(heroID):
    #            localizedname = hero.findtext("localized_name")
    #return localizedname


#def getAllHeroes():
#    herolist = {}
#    with open("heroes.xml",'r') as r:
#        tree = ET.fromstring(r.read().encode('ascii', 'ignore'))
#        heroes = tree.find("heroes").findall("hero")
#        for hero in heroes:
#            herolist[hero.findtext('id')] = hero.findtext('localized_name')
#    return herolist

def getHeroesPlayedAs(myID,matchdetails = None):
    herolist = []
    if matchdetails is None:
        matchdetails = openDetails(myID)
    for match in matchdetails:
        tree = ET.fromstring(match.encode('ascii', 'ignore'))
        players =tree.find("players").findall("player")
        try:
            for player in players:
                if player.find("account_id").text == myID:
                    curhero = player.findtext("hero_id")
                    if curhero not in herolist:
                        herolist.append(curhero)
        except:
            #print "player not found in match " + tree.findtext("match_id")
            print(match)
    return herolist
                    
def getHeroesNotPlayedAs(myID, localized = True, matchdetails = None):
    heroesnotplayedas = []
    heroesplayedas = getHeroesPlayedAs(myID,matchdetails)
    allheroes = getAllHeroes()
    if localized:
        for hero in allheroes:
            if hero not in heroesplayedas:
                heroesnotplayedas.append(getHero(hero))
    else:
        for hero in allheroes:
            if hero not in heroesplayedas:
                heroesnotplayedas.append(hero)
    return heroesnotplayedas

def printMatchSummary(match): #unfinished method
    """enter a match, get a summary of player names, heroes, kda, items, abilities
    basically everything in a nice ui.
    example usage: matchSummary(openDetails(mabufula)[0])"""
    tree = ET.fromstring(match.encode('ascii', 'ignore'))
    players = tree.find("players").findall("player")
    for player in players:
        print("--------------------")
        #print player.find("player_slot").text
        #hero = player.find("hero_id").text
        children = player.getchildren()
        for child in children:
            ctag = child.tag
            ctext = child.text
            if ctag[:4]=="item": #can replace with case but how 2 do in python?
                if ctext == '0':
                    print("")
                else:
                    print("    {}".format(ITEMS[ctext]))
            elif ctag == "account_id":
                try:
                    r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
                                     "format=%s"
                                     "&key=%s"
                                     "&steamids=%s"%("XML",apikey,int(ctext)+76561197960265728))
                    tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
                    player =tree.find("players").find("player")
                    try:
                        print(player.findtext('personaname')) 
                    except:
                        print("???????")
                except:
                    print("error retrieving player name. check net connection")
            elif ctag == "hero_id":
                print(getHero(ctext)) #can streamline this with getAllHeroes
            else:
                print(ctag + ": " + ctext)#most are self-explanatory

                #what it should look like
"""mabufula
Storm Spirit
kills/deaths/assists: 12/4/8
level: 22
---
bottle
arcane_boots
bloodstone
dagon_4
---
leaver_status: 0
gold: 59
last_hits/denies: 54/0
gold_per_min: 463
xp_per_min: 834
gold_spent: 14877
hero_damage: 17813
tower_damage: 93
hero_healing: 0"""

def treeToDict(tree):
    """converts an ET to a dict, appending duplicately named tags with
    sequential numbers when setting them as tags of the dict"""
    dic = {}
    for c in tree.getchildren():
        ctag=c.tag
        if ctag in dic:
            n=1
            while ctag in dic:
                n+=1
                ctag=c.tag+str(n)
        if c.getchildren()==[]:
                    
            dic[ctag]=c.text
        else:
            dic[ctag]=treeToDict(c)
    return dic

def selectDetails(matchdetails,players=None,items=None,heroes=None,evalstring=None):
    """from a list of matchedetails, this function returns the matchedetails that contain
    all? of the listed things and evaluates true for the evalstring."""
    #maybe I should just create an SQL database instead of parsing these elements.... nahhhh
    for match in matchdetails:
        toplevel = {}
        plevel = {}
        tree = ET.fromstring(match.encode('ascii', 'ignore'))
        for fact in tree.getchildren():
            if fact.getchildren==[]:
                toplevel[fact.tag]=fact.text
            else:
                toplevel[fact.tag]={}
        print(toplevel)
        players = tree.find("players").findall("player")
        for player in players:
           
            children = player.getchildren()
            for child in children:
                ctag = child.tag
                ctext = child.text
                if ctag[:4]=="item": #can replace with case but how 2 do in python?
                    print(ITEMS[ctext])
                elif ctag == "account_id":
                    try:
                        r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
                                         "format=%s"
                                         "&key=%s"
                                         "&steamids=%s"%("XML",apikey,int(ctext)+76561197960265728))
                        tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
                        player =tree.find("players").find("player")
                        try:
                            print(player.findtext('personaname')) 
                        except:
                            print("???????")
                    except:
                        print("error retrieving player name. check net connection")
                elif ctag == "hero_id":
                    print(getHero(ctext)) #can streamline this with getAllHeroes
                else:
                    print(ctag + ": " + ctext)#most are self-explanatory


def boots(user=girlgamer):
    print(findAllGamesWithItem(user,"50") ) 
    print(findAllGamesWithItem(user,"214") ) 
    findAllGamesWithItem(user,"180")  
    print(findAllGamesWithItem(user,"48")  )
    print(findAllGamesWithItem(user,"63"))
    print(findAllGamesWithItem(user,"162"))
    


#saveAllDetailsFromID(mabufula)
#saveAllDetailsFromID("29065860")
#saveAllDetailsFromID("47199737")
