

Name: lingobot
Author: John McLean
Purpose: To interact between irc channel using different language and translate between them.

To run, simply cd to the directory containing lingobot.py, and run './lingobot.py' or 'python lingobot.py'.  Requires python and python-irclib to run. Upon running, lingobot prompts for initial channels it should join.  Specify channels in one line separated by commas and a space (ie. #fedora-meeting-en, #fedora-meeting-es, #lingobot-test).  

Lingobot will translate any public channel messages, topic changes, mode changes, and users joining and leaving.  If lingobot is invited to a channel, it will auto-connect, but you must specifiy the language the channel is using immediately: "/msg lingobot <channel> <language>"

Valid languages:
arabic - ar
chinese - zh
german - de
english - en
french - fr
hebrew - he
hindi - hi
italian - it
japanese - ja
korean - ko 
latin - la
portugese - pt
romanian - ro
russian - ru
serbian -sr
spanish - es
slovenian - sl
swedish - sv
turkish - tr
