#MASKOFMADNESS.COM
#GGBRANCH.COM
#DAGON5.COM

import requests
import os
import pickle
import xml.etree.ElementTree as ET
import items
itemray = items.itemray

mabufula = "40753485"
arthor = "47199737"
flameant = "29065860"
girlgamer = "128596275"

with open("config.txt", 'r') as f:
    apikey = f.read()

def getAllMatches(playerid):
    matchlist = []
    ia=0
    sequence = 0
    maxmatch = "9999999999"
    #maxmatch = "112822135"
    go = True

    while go == True:
        sequence+=1
        maxmatch = str(int(maxmatch)-1)
        r = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?"
                         "format=%s"
                         "&key=%s"
                         "&account_id=%s"
                         "&matches_requested=%s"
                         "&start_at_match_id=%s"%("XML",apikey,playerid,"60",maxmatch))
        tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
        matches=tree.find("matches").findall("match")
        if not matches:
            go = False
        for h in matches:
            ia+=1
            #fdsa = h.find("players").findall("player")
            templist = []
            maxmatch = h.find("match_id").text
            #print templist
            matchlist.append(maxmatch)
            print maxmatch
    #print r.text
    print "matches: " + str(ia)
    print "sequence: " + str(sequence)
    return matchlist

def saveAllMatches(playerID,overwrite = True):
    try:
        with open("matches"+str(playerID)+".txt",'r') as p:
            pass
    except IOError:
        allmatches = getAllMatches(playerID)
        with open("matches"+str(playerID)+".txt",'w') as p:
            pickle.dump(allmatches,p)
    else:
        if overwrite:
            allmatches = getAllMatches(playerID)
            with open("matches"+str(playerID)+".txt",'w') as p:
                pickle.dump(allmatches,p)
        else:
            pass

def getAllDetails(matchfile):
    allDetailsXML = []
    with open(matchfile, 'r') as f:
        matchlist = pickle.load(f)
    for i in matchlist:
        try:
            r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
                             "?format=%s"
                             "&key=%s"
                             "&match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",i))
        except:
            print "failed. " + i + ". Trying again."
            try:
                r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
                                 "?format=%s"
                                 "&key=%s"
                                 "&match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",i))
            except:
                print "failed again.  skipping."
        allDetailsXML.append(r.text)
        #print r.text
        print i
    return allDetailsXML

def saveAllDetails(playerID,overwrite = True):
    try:
        with open("matchdetails"+str(playerID)+".txt",'r') as q:
            #if this doesn't raise an error, then the file already exists
            print "FILE EXISTS"
            pass
        
    except IOError:
        #this probably means that the file doesn't exist yet.
        print "FILE DOESN'T EXIST YET.  WRITING."
        alldetails = getAllDetails("matches"+str(playerID)+".txt")
        with open("matchdetails"+str(playerID)+".txt",'w') as p:
            pickle.dump(alldetails,p)
    else:
        #if the file already exists
        if overwrite:
            print "OVERWRITING"
            alldetails = getAllDetails("matches"+str(playerID)+".txt")
            with open("matchdetails"+str(playerID)+".txt",'w') as p:
                pickle.dump(alldetails,p)
        else:
            print "NOT OVERWRITING"
            pass
        
def openDetails(playerID):
    with open("matchdetails"+str(playerID)+".txt", 'r') as f:
        matchdetails = pickle.load(f) 
    return matchdetails

def saveAllDetailsFromID(playerID,overwrite = True):
    print "saving all matches"
    saveAllMatches(playerID,overwrite)
    print "saving all details"
    saveAllDetails(playerID,overwrite)

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
            for i in xrange(0,5):
                curitem = user.find("item_"+str(i))
                if curitem.text == str(item):
                    amount+=1
                    #print getHero(player.findtext("hero_id")) + " - " + tree.findtext("match_id")
                    itemmatches.append(tree.findtext("match_id"))
                    itemmatchdetails.append(match)
                    #print "http://dotabuff.com/matches/"+tree.findtext("match_id")
                    break
        except:
            print "user not found in game " + tree.findtext("match_id")
    print str(amount) + " games with "+ itemray[str(item)]
    return itemmatchdetails

def calculateWinrateFromDetails(myID, matchdetails):
    wins = 0
    for match in matchdetails:
        tree = ET.fromstring(match.encode('ascii', 'ignore'))
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
            print "user not found"
        if radiant == tree.findtext('radiant_win'):
            wins+=1
    try:
        winpercent = round(float(100*wins)/len(matchdetails),1)
        print str(wins) + "/" + str(len(matchdetails)) + " - " + str(winpercent) + "%"
    except ZeroDivisionError:
        #hey it's pythonic!
        winpercent = -1
        print "never bought!"
    return (wins,len(matchdetails),winpercent)

def calculateWinrate(myID, item):
    return calculateWinrateFromDetails(myID,findAllGamesWithItem(myID,item))

def calculateWinrateForAllItems(myID):
    winrates = []
    iteration = 0
    for i in itemray:
        print str(iteration) + " out of " + str(len(itemray))
        iteration+=1
        winrates.append((i,calculateWinrate(myID,i)))
    sortList(winrates)
    print winrates
    for winrate in winrates:
        print str(winrate[1][2]) + "%  - " + itemray[str(winrate[0])] + " - " + str(winrate[1][0]) + "/" + str(winrate[1][1])
        
def sortList(asdf):
    asdf.sort(key=lambda price: price[1][2])

def getHero(heroID):
    with open("heroes.xml",'r') as r:
        tree = ET.fromstring(r.read().encode('ascii', 'ignore'))
        heroes = tree.find("heroes").findall("hero")
        for hero in heroes:
            if hero.findtext("id")==str(heroID):
                localizedname = hero.findtext("localized_name")
    return localizedname

def boots(user=girlgamer):
    #print findAllGamesWithItem(user,"50")  
    #print findAllGamesWithItem(user,"214")  
    #findAllGamesWithItem(user,"180")  
    #print findAllGamesWithItem(user,"48")  
    #print findAllGamesWithItem(user,"63")
    print findAllGamesWithItem(user,"162")
    


#saveAllDetailsFromID(mabufula)
#saveAllDetailsFromID("29065860")
#saveAllDetailsFromID("47199737")
