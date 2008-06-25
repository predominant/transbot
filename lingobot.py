#!/usr/bin/python

######################################################################
#	Name: lingobot
#	Author: John McLean
#	
#	This program connects to user-designated irc channels and translate
# between them.  ie. if one channel is in English and one in Spanish, anything 
#said in the English channel shows up in Spanish in the Spanish channel. 
#This works with multiple channels and multiple users.  Users must designate 
#the channel's language, either by placing channel:language pairs into the 
#dictionary below or messaging the bot designating language 
#(/msg lingobot <channel> <language> (en, es, fr, ru, zh, etc.))
######################################################################

import irclib, urllib2, urllib, re

irclib.DEBUG = True



#connection info and default values
network = 'irc.freenode.net'
port = 6667
channel_languages = {"#fedora-meeting":"en", "#fedora-meeting-en":"en", "#fedora-meeting-es":"es", "#fedora-meeting-pt":"pt", "#fedora-meeting-fr":"fr", "#fedora-meeting-ru":"ru", "#fedora-meeting-zh":"zh"}
supported_languages = [ 'de' , 'zh' , 'en' , 'es' , 'fr' , 'ru' , 'pt' , 'ga' , 'hi' , 'he' , 'it' , 'ko' , 'la' , 'ro' , 'sr' , 'sl' , 'sv' , 'tr' , 'ar' , 'ja' ]
prompt = raw_input("Choose your channels (separate by ', '): ")
channels = prompt.split( ", " )
nick = 'lingobot'
name = 'Lingobot Test'

def translator(source_lang, target_lang, message, name, channel):
	url = 'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=' + urllib2.quote(message) + '&langpair=' + source_lang + '%7C' + target_lang
	urlRetVal = urllib2.urlopen(url)
	for line in urlRetVal:
		line = line.replace('{"responseData": {"translatedText":"', '');line = line.replace('"}, "responseDetails": null, "responseStatus": 200}', '')
		return line

#Generic echo handler (space added, then with no space), used to ouput initial info from server
def handleEcho ( connection, event ):
	print
	print " ".join ( event.arguments() )
def handleNoSpace ( connection, event ):
	print " ".join ( event.arguments() )

#handles topic changes
def handleTopic ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ event.target() ] 
	message = event.arguments() [ 0 ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has set mode:" + message, name, channel)
			server.privmsg ( channel, name + " " + translation )
#handles mode changes
def handleMode ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ event.target() ] 
	message = event.arguments() [ 0 ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has set mode:" + message, name, channel)
			if len ( event.arguments() ) < 2:
				server.privmsg ( channel, name + " " + translation)
			else:
				name2 = events.arguments() [ 1 ]
				server.privmsg ( channel, name + " " + translation.split( "has set " ) [ 0 ] + name2 + "'s" + translation.split( "has set" ) [ 1 ] )

#handles Parts
def handlePart ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ event.target() ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has quit", name, channel)
			server.privmsg ( channel, name + " " + translation + " " + event.target() )
#handles quits
def handleQuit ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ event.target() ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has disconnected:", name, channel)
			server.privmsg ( channel, name + " " + translation + " " + event.target() )
	
#handles kicks
def handleKick ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	name2 = event.arguments() [ 0 ]
	source_lang = channel_languages [ event.target() ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has been kicked by", name, channel)
			server.privmsg ( channel, name2 + " " + translation + " " + name)
#handle private notices
def handlePrivNotice ( connection, event ):
	if event.source():
		print ":: " + event.source() + " ->" + event.arguments() [ 0]
	else:
		print event.arguments() [ 0 ]
#handle channel joins
def handleJoin ( connection, event ):
	#the source needs to be split into just the name
	#it comes in the format nickname!user@host
	name = event.source().split ( "!" ) [ 0 ] 
	if name == "lingobot":
		return
	source_lang = channel_languages [ event.target() ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has joined:", name, channel)
			server.privmsg ( channel, name + ' ' + translation + ' ' + event.target() )


#auto-joins to invited channels
def handleInvite ( connection, event ):
	channels.append ( event.arguments() [ 0 ] )
	connection.join ( event.arguments() [ 0 ] ) 


#handles private messages
def handlePrivMessage (  connection, event ):
	name = event.source().split ( '!' ) [ 0 ]
	command = event.arguments() [ 0 ].split()
	try:
		if command[1] in supported_languages:
			 channel_languages [ command [ 0 ] ] = command [ 1 ]
	except: 
		server.privmsg ( name , command + ": unrecognized command" )

#handles public messages
def handlePubMessage ( connection, event ):
	source_lang = channel_languages [ event.target() ] 
	message = event.arguments() [ 0 ]
	name = event.source().split( '!' ) [ 0 ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			line = translator(source_lang, target_lang, message, name, channel)
			server.privmsg(channel, name +  "> " + line)
#create an irc object
irc = irclib.IRC()

# Register handlers
irc.add_global_handler ( 'part' , handlePart ) #handles parts
irc.add_global_handler ( 'quit' , handleQuit ) #handles quits
irc.add_global_handler ( 'kick' , handleKick ) #handles kicks
irc.add_global_handler ( 'mode' , handleMode ) #handles mode changes
irc.add_global_handler ( 'topic' , handleTopic ) #handles topic changes
irc.add_global_handler ( 'privmsg', handlePrivMessage ) #private messages
irc.add_global_handler ( 'pubmsg', handlePubMessage ) #public channel messages
irc.add_global_handler ( 'invite', handleInvite ) #invite
irc.add_global_handler ( 'privnotice', handlePrivNotice ) #Private notice
irc.add_global_handler ( 'welcome', handleEcho ) # Welcome message
irc.add_global_handler ( 'yourhost', handleEcho ) # Host message
irc.add_global_handler ( 'created', handleEcho ) # Server creation message
irc.add_global_handler ( 'myinfo', handleEcho ) # "My info" message
irc.add_global_handler ( 'featurelist', handleEcho ) # Server feature list
irc.add_global_handler ( 'luserclient', handleEcho ) # User count
irc.add_global_handler ( 'luserop', handleEcho ) # Operator count
irc.add_global_handler ( 'luserchannels', handleEcho ) # Channel count
irc.add_global_handler ( 'luserme', handleEcho ) # Server client count
irc.add_global_handler ( 'n_local', handleEcho ) # Server client count/maximum
irc.add_global_handler ( 'n_global', handleEcho ) # Network client count/maximum
irc.add_global_handler ( 'luserconns', handleEcho ) # Record client count
irc.add_global_handler ( 'luserunknown', handleEcho ) # Unknown connections
irc.add_global_handler ( 'motdstart', handleEcho ) # Message of the day ( start )
irc.add_global_handler ( 'motd', handleNoSpace ) # Message of the day
irc.add_global_handler ( 'edofmotd', handleEcho ) # Message of the day ( end )
irc.add_global_handler ( 'join', handleJoin ) # Channel join
irc.add_global_handler ( 'namreply', handleNoSpace ) # Channel name list
irc.add_global_handler ( 'endofnames', handleNoSpace ) # Channel name list ( end )

#create a server object, connect and join the channel
server = irc.server()
server.connect ( network, port, nick, ircname = name ) 
for channel in channels:
	server.join ( channel )

#jump into infinite loop
irc.process_forever()

print "hi", "howdy"
