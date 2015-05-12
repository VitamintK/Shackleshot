import Shackleshot
from Shackleshot import itemray, apikey
import random
import requests
import xml.etree.ElementTree as ET

matchez = Shackleshot.openDetails(Shackleshot.mabufula)
random_match = random.choice(matchez)
#Shackleshot.printMatchSummary(random_match)
tree = ET.fromstring(random_match.encode('ascii', 'ignore'))
players = tree.find("players").findall("player")
random_player = random.choice(players)

children = random_player.getchildren()
for child in children:
    ctag = child.tag
    ctext = child.text
    if ctag[:4]=="item": #can replace with case but how 2 do in python?
        if ctext == '0':
            print("")
        else:
            print("    {}".format(itemray[ctext]))
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
            raise
            print("error retrieving player name. check net connection")
    elif ctag == "hero_id":
        
        #DO NOT OUTPUT HERO NAME.  This is for players to guess.
        random_hero = Shackleshot.getHero(ctext) #can streamline this with getAllHeroes
    else:
        print(ctag + ": " + ctext)#most are self-explanatory

guess = input("What hero was this? (case insensitive) ")
if random_hero.lower() == guess.lower():
    print("YOU WERE RIGHT")
else:
    print("YOU WERE WRONG.  The hero was {}".format(random_hero.lower()))
