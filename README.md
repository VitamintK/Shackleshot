Shackleshot
===========

Shackleshot.py is a Python module utilizing Valve's [Dota 2 API](http://dev.dota2.com/showthread.php?t=47115) to perform a variety of calculations and functons.
Currently, it can return a list of all matches, and match details played by a player, given their 32-bit ID.
From these match details, it can return lists of all match details where a specified user bought a given item, or every match where a given player was in the same match with another given player. 
From any set of match details, including all matches with a certain item, or all matches with a certain played, it can calculate the winrate.

##How to Use

Alright, I wrote this in 2013 when I was newish to coding, so it's pretty kludgy.  If you want to use it, though, here's how:  
Edit config.txt with your Dota 2 API key.  Run Shackleshot.py.   
To save a player's match history to files, use the function ```saveAllDetailsFromID(player_steam_id)``` where  player_steam_id is your "Steam 3 ID" which can be found [here](http://steamidfinder.com/).

```
myID = '40753485'
saveAllDetailsFromID(myID)
```

You can then use the various analysis functions to find out cool stuff.  
To print a list of all players you've played with more than one time before:

```
myID = '40753485'
calculatePlayedWithFromDetails(myID)
```

To calculate your winrate with a certain player on your team

```
myID, friendID = '40753485', '29065860'
my_games_with_jon, my_games_against_jon = getPlayedWith(myID,friendID)
print(calculateWinrateFromDetails(myID,my_games_with_jon)
```

To print all your item winrates (although Dotabuff has since added this feature too):

```
calculateWinrateForAllItems(myID)
```


Dota Crack
===========
Although Dota Crack is sorta a separate project, it is included in this repo for convenience because it imports Shackleshot.py.   Dota Crack is prototype for a Flask webapp trivia game.  The flask application is DotaTriviaFlaskApp.py, and it uses Shackleshot.py to get match data.  A prototype is currently located at http://kevinwang4.pythonanywhere.com
