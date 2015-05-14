import Shackleshot
from Shackleshot import itemray, apikey
import random
import requests
import xml.etree.ElementTree as ET
import datetime

#IDEA!!!!: THE CHOICES YOU ARE GIVEN ARE THE 10 HEROES IN THE GAME.  OR.  YOU HAVE TO MATCH EACH OF THE 10 HEROES WITH THEIR STATS.

def random_trivia(out_format="html"):
    matchez = Shackleshot.openDetails(Shackleshot.mabufula)
    random_match = random.choice(matchez)
    #Shackleshot.printMatchSummary(random_match)
    tree = ET.fromstring(random_match.encode('ascii', 'ignore'))

    import xml.dom.minidom as minidom
    rough_string = ET.tostring(tree, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    print(reparsed.toprettyxml(indent="\t")), 'df'


    players = tree.find("players").findall("player")
    random_player = random.choice(players)

    kda = dict()
    match_id = tree.find("match_id").text
    pretty_string =  datetime.datetime.fromtimestamp(int(tree.find("start_time").text)).strftime('%Y-%m-%d %H:%M:%S') + '\n'
    children = random_player.getchildren()
    for child in children:
        ctag = child.tag
        ctext = child.text
        if ctag[:4]=="item": #can replace with case but how 2 do in python?
            if ctext == '0':
                if(out_format == "html"):
                    pretty_string += '<img class="item" src="static/blank_item.png">'
                else:
                    pretty_string +=("")
            else:
                if(out_format == "html"):
                    pretty_string +=('<img class="item" src="http://cdn.dota2.com/apps/dota2/images/items/{}_lg.png">'.format(itemray[ctext]))
                else:
                    pretty_string +=("    {}".format(itemray[ctext])) + '\n'
            if out_format == 'html' and (ctag[-1:] == '2' or ctag[-1:] == '5'):
                pretty_string += '\n'
        elif ctag == "account_id":
            try:
                r = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
                                 "format=%s"
                                 "&key=%s"
                                 "&steamids=%s"%("XML",apikey,int(ctext)+76561197960265728))
                btree = ET.fromstring(r.text.encode('ascii', 'ignore'))
                player =btree.find("players").find("player")
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
        elif ctag == "kills" or ctag=="assists" or ctag == "deaths":
            kda[ctag] = ctext
            if len(kda) == 3:
                kdastr = "k/d/a: {}/{}/{}".format(kda['kills'], kda['deaths'], kda['assists'])
                pretty_string += kdastr + '\n'
        else:
            pretty_string += (ctag + ": " + ctext) + '\n'#most are self-explanatory
    pretty_string += "game duration: {} minutes".format(int(int(tree.find("duration").text)/60))
    return pretty_string, random_hero, match_id
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
