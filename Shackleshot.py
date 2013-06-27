import requests
import os
import pickle
import xml.etree.ElementTree as ET
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
                         "&start_at_match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",playerid,"60",maxmatch))
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
def saveAllMatches():
    allmatches = getAllMatches("40753485")
    #print allmatches
    with open("matchlist.txt",'w') as p:
        pickle.dump(allmatches,p)

def getAllDetails(matchfile):
    allDetailsXML = []
    with open(matchfile, 'r') as f:
        matchlist = pickle.load(f)
    for i in matchlist:
        r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
                         "?format=%s"
                         "&key=%s"
                         "&match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147",i))
        allDetailsXML.append(r.text)
        #print r.text
        print i
    return allDetailsXML

def saveAllDetails():
    alldetails = getAllDetails("matchlist.txt")
    with open("matchdetails.txt",'w') as p:
        pickle.dump(alldetails,p)

def openDetails():
    with open("matchdetails.txt", 'r') as f:
        matchdetails = pickle.load(f) 
    return matchdetails

def findAllGamesWithItem(myID,item):
    matchdetails = openDetails()
    for match in matchdetails:
        try:
            tree = ET.fromstring(match.encode('ascii', 'ignore'))
            players =tree.find("players").findall("player")
            for player in players:
                user = player.find("account_id")
                if user.text == myID:
                    break
        except:
            print "user not found in game " + match
        for i in xrange(0,5):
            curitem = player.find("item_"+str(i))
            if curitem.text == str(item):
                print tree.findtext("match_id")
                break
            
        

findAllGamesWithItem("40753485","116")
    
