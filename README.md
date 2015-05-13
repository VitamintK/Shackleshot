Shackleshot
===========

Shackleshot is a Python module utilizing Valve's [Dota 2 API](http://dev.dota2.com/showthread.php?t=47115) to perform a variety of calculations and functons.
Currently, it can return a list of all matches, and match details played by a player, given their 32-bit ID.
From these match details, it can return lists of all match details where a specified user bought a given item, or every match where a given player was in the same match with another given player. 
From any set of match details, including all matches with a certain item, or all matches with a certain played, it can calculate the winrate. 

Dota Crack
===========
Because I'm lazy, this repo also contains a prototype for a Flask webapp trivia game.  The flask application is DotaTriviaFlaskApp.py, and it uses Shackleshot.py to get match data.  A prototype is currently located at http://www.kevinwang4.pythonanywhere.com
