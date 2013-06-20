import requests
import xml.etree.ElementTree as ET

ia=0
sequence = 0
#maxmatch = "9999999999"
maxmatch = "12822135"
go = True
#def getHistory():

while go == True:
    sequence+=1
    maxmatch = str(int(maxmatch)-1)
    r = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?"
                     "format=%s"
                     "&key=%s"
                     "&account_id=%s"
                     "&matches_requested=%s"
                     "&start_at_match_id=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147","40753485","60",maxmatch))
    tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
    matches=tree.find("matches").findall("match")
    if matches:
        go = False
    for h in matches:
        ia+=1
        #fdsa = h.find("players").findall("player")
        templist = []
        if h.find("match_id").text == maxmatch:
            go = False
        maxmatch = h.find("match_id").text
        #print templist
        print maxmatch
    #if sequence == 3:
    #break
#print r.text
print ia
print "sequence " + str(sequence)
