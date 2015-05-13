import Shackleshot
from Shackleshot import itemray, apikey
import random
import requests
import xml.etree.ElementTree as ET


#IDEA!!!!: THE CHOICES YOU ARE GIVEN ARE THE 10 HEROES IN THE GAME.  OR.  YOU HAVE TO MATCH EACH OF THE 10 HEROES WITH THEIR STATS.

def random_trivia(out_format="html"):
    matchez = Shackleshot.openDetails(Shackleshot.mabufula)
    random_match = random.choice(matchez)
    #Shackleshot.printMatchSummary(random_match)
    tree = ET.fromstring(random_match.encode('ascii', 'ignore'))
    players = tree.find("players").findall("player")
    random_player = random.choice(players)

    pretty_string = ''
    children = random_player.getchildren()
    for child in children:
        ctag = child.tag
        ctext = child.text
        if ctag[:4]=="item": #can replace with case but how 2 do in python?
            if ctext == '0':
                pretty_string +=("") + '\n'
            else:
                if(out_format == "html"):
                    pretty_string +=('<img src="http://cdn.dota2.com/apps/dota2/images/items/{}_lg.png">'.format(itemray[ctext]))
                    if ctag[-1:] == '2' or ctag[-1:] == '5':
                        pretty_string += '\n'
                else:
                    pretty_string +=("    {}".format(itemray[ctext])) + '\n'
        elif ctag == "account_id":
            try:
                r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
                                 "format=%s"
                                 "&key=%s"
                                 "&steamids=%s"%("XML",apikey,int(ctext)+76561197960265728))
                tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
                player =tree.find("players").find("player")
                try:
                    pretty_string += (player.findtext('personaname'))  + '\n'
                except:
                    pretty_string += ("???????") + '\n'
            except:
                raise
                pretty_string += ("error retrieving player name. check net connection") + '\n'
        elif ctag == "hero_id":
            
            #DO NOT OUTPUT HERO NAME.  This is for players to guess.
            random_hero = Shackleshot.getHero(ctext) #can streamline this with getAllHeroes
        else:
            pretty_string += (ctag + ": " + ctext) + '\n'#most are self-explanatory
    return pretty_string, random_hero
    #guess = input("What hero was this? (case insensitive) ")
    #if random_hero.lower() == guess.lower():
    #    print("YOU WERE RIGHT")
    #else:
    #    print("YOU WERE WRONG.  The hero was {}".format(random_hero.lower()))

if __name__ == '__main__':
    print(random_trivia())
    guess = input("What hero was this? (case insensitive) ")
    if random_hero.lower() == guess.lower():
        print("YOU WERE RIGHT")
    else:
        print("YOU WERE WRONG.  The hero was {}".format(random_hero.lower()))

#more info needed: date, gamelength, etc.
