import requests
import xml.etree.ElementTree as ET

improductive= []
ia=0
#def getHistory():

while True:
    r = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?"
                     "format=%s"
                     "&key=%s"
                     "&account_id=%s"
                     "&matches_requested=%s"%("XML","9D6AA7810AF5EF66B3A70566614DE147","40753485","60"))
    tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
    matches=tree.find("matches").findall("match")
    for h in matches:
        ia+=1
        fdsa = h.find("players").findall("player")
        templist = []
        maxmatch = h.find("match_id").text
        """for i in fdsa:
            #improductive.append(i.find("level").text)
            try:
                if i.find("account_id").text == "4294967295":
                    templist.append("1")
                else:
                    templist.append( i.find("account_id").text)
            except:
                templist.append("0")"""
        #print templist
        print maxmatch
    break
#print r.text
print improductive
print ia
