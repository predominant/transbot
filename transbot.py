#!/usr/bin/python
######################################################################
#	Name: transbot
#	Author: John McLean
#	
#	This program connects to user-designated irc channels and translate
# between them.  ie. if one channel is in English and one in Spanish, anything 
#said in the English channel shows up in Spanish in the Spanish channel. 
#This works with multiple channels and multiple users.  Users must designate 
#the channel's language, either by placing channel:language pairs into the 
#dictionary below or messaging the channel designating the language 
#according to the format: ".<lang_abbreviation>" for example: ".en" or ".es"
######################################################################




import irclib, urllib2, urllib, re, sys, os, codecs
from htmlentitydefs import name2codepoint

irclib.DEBUG = True

#connection info and default values
network = 'irc.freenode.net'
port = 6667
channel_languages = {"#fedora-meeting":"en", "#fedora-meeting-en":"en", "#fedora-meeting-es":"es", "#fedora-meeting-pt":"pt", "#fedora-meeting-fr":"fr", "#fedora-meeting-ru":"ru", "#fedora-meeting-zh":"zh"}
supported_languages = [ 'de' , 'zh' , 'en' , 'es' , 'fr' , 'ru' , 'pt' , 'ga' , 'hi' , 'he' , 'it' , 'ko' , 'la' , 'ro' , 'sr' , 'sl' , 'sv' , 'tr' , 'ar' , 'ja' ]
channels = []
try:
	conf_size = os.path.getsize ( '/etc/transbot.conf' )
except:
	conf_size = 0
if conf_size is not 0:
	conf_file = open ( '/etc/transbot.conf' )
	network = conf_file.readline().split ( ':' ) [ 1 ]
	network = network.strip ()
	channel_list = conf_file.readline().split ( ':' ).lower() [ 1 ]
	chans = channel_list.split ( ',' )
	for channel in chans:
		channel_languages [ channel.split() [ 0 ] ] = channel.split() [ 1 ]
		channels.append ( channel.split() [ 0 ] )
	port = int ( conf_file.readline().split ( ':' ) [ 1 ] )
	conf_file.close()

for channel in sys.argv [ 1: ]:
	channels.append ( "#" + str ( channel ) )
for channel in channels:
	if channel in channel_languages:
		pass
	else:
		channel_languages [ channel ] = "en"
nick = 'transbot0'
name = 'transbot Test'


#Handles the actual translation of the message
def translator(source_lang, target_lang, message, name, channel):
	url = 'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=' + urllib2.quote(message) + '&langpair=' + source_lang + '%7C' + target_lang
	urlRetVal = urllib2.urlopen(url)
	for line in urlRetVal:
		line = line.replace('{"responseData": {"translatedText":"', '');line = line.replace('"}, "responseDetails": null, "responseStatus": 200}', '')
	line = unicode ( line, "utf-8" )
	line = line.encode ( "utf-8 " )
	_entity_re = re.compile(r'&(?:(#)(\d+)|([^;]+));') 
	def _repl_func(match):
		if match.group(1): # Numeric character reference
			return unichr(int(match.group(2)))
		else:
			return unichr(name2codepoint[match.group])
	print _entity_re.sub (_repl_func, line ) 
	return _entity_re.sub ( _repl_func, line )


#Generic echo handler (space added, then with no space), used to ouput initial info from server
def handleEcho ( connection, event ):
	print
	print " ".join ( event.arguments() )
def handleNoSpace ( connection, event ):
	print " ".join ( event.arguments() )


#handle private notices
def handlePrivNotice ( connection, event ):
	if event.source():
		print ":: " + event.source() + " ->" + event.arguments() [ 0]
	else:
		print event.arguments() [ 0 ]


#auto-joins to invited channels
def handleInvite ( connection, event ):
	channels.append ( event.arguments() [ 0 ] )
	channel_languages [ str ( event.arguments() [ 0 ]  ).lower() ] = '.en'
	connection.join ( event.arguments() [ 0 ] ) 


#handles private messages
def handlePrivMessage (  connection, event ):
	name = event.source().split ( '!' ) [ 0 ]
	helpmessage =  [ 'transbot 0.1', "This program connects to user specified channels on irc.freenode.net and translates between languages on those channels. Users must specify the language on the channel before transbot will translate anything. Specification comes in the form of messaging the channel with a message of the form '.<language abbreviation>'. For example, english is '.en', spanish is '.es'. ", 'Languages supported are: ar - Arabic, de - German, en - English, es - Spanish, fr - French, ga - Irish, hi - Hindi, he - Hebrew, it - Italian, ja - Japanese, ko - Korean, la - Latin, pt - Portugese, ro - Romanian, ru - Russian, sl - Slovenian, sr - Serbian, sv - Swedish, tr - Turkish, zh - Chinese' ]
	for line in range ( len ( helpmessage ) ):	
		server.privmsg ( name , helpmessage [ line ] )


#handles public messages
def handlePubMessage ( connection, event ):
	seeker = re.compile ( '^\.[a-zA-Z]{2}$' )
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
	message = event.arguments() [ 0 ]
	name = event.source().split( '!' ) [ 0 ] 
	if name.strip ( '0123456789' ) == 'transbot':
		return
	if bool ( seeker.search ( message ) ):
		message = message.strip ( '.' )
		channel_languages [ str ( event.target() ).lower()  ] = message; return
	for channel in channels:
		if channel_languages [ channel ] == source_lang:
			pass
		else:
			target_lang = channel_languages [ channel ]
			line = translator(source_lang, target_lang, message, name, channel)
			server.privmsg(channel, name +  "> " + line)


#handles topic changes
def handleTopic ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
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
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
	message = event.arguments() [ 0 ] 
	for channel in channels:
		if channel_languages [ channel ] == source_lang:
			pass
		else:
			target_lang = channel_languages [ channel ]
			translation = translator(source_lang, target_lang, "has set mode:" + message, name, channel)
			if len ( event.arguments() ) < 2:
				server.privmsg ( channel, name + " " + translation)
			else:
				name2 = events.arguments() [ 1 ]
				server.privmsg ( channel, name + " " + translation.split( "has set " ) [ 0 ] + name2 + "'s" + translation.split( "has set" ) [ 1 ] )


#handles Parts
def handlePart ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has quit", name, channel)
			server.privmsg ( channel, name + " " + translation + " " + str ( event.target() ).lower()  )


#handles quits
def handleQuit ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	for channel in channels:
		target_lang = channel_languages [ channel ]
		translation = translator( 'en' , target_lang, "has disconnected", name, channel)
		server.privmsg ( channel, name + " " + translation )
	
	
#handles kicks
def handleKick ( connection, event ):
	name = event.source().split ( "!" ) [ 0 ]
	name2 = event.arguments() [ 0 ]
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
	for channel in channels:
		if channel_languages[channel] == source_lang:
			pass
		else:
			target_lang = channel_languages[channel]
			translation = translator(source_lang, target_lang, "has been kicked by", name, channel)
			server.privmsg ( channel, name2 + " " + translation + " " + name)


#handle channel joins
def handleJoin ( connection, event ):
	#the source needs to be split into just the name
	#it comes in the format nickname!user@host
	name = event.source().split ( "!" ) [ 0 ] 
	if name.strip ( '0123456789' ) == "transbot":
		return
	source_lang = channel_languages [ str ( event.target() ).lower()  ] 
	for channel in channels:
		if channel_languages [ channel ] == source_lang:
			pass
		else:
			target_lang = channel_languages [ channel ]
			translation = translator(source_lang, target_lang, "has joined:", name, channel)
			server.privmsg ( channel, name + ' ' + translation + ' ' + str ( event.target() ).lower()  )

#handler for a pre-registed nick
def handleNoNick (connection, event):
	global nick, server
	instance = int ( nick.strip ( 'transbot' ) )
	instance += 1
	nick2 = 'transbot' + str ( instance )
	server = server_object ( network, nick2, name, port, ircname = name )
	return server
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
irc.add_global_handler ( 'nicknameinuse', handleNoNick ) #handles pre-registered nick

#create a server object, connect and join the channel
def server_object ( network, nick, name, port, ircname ):
	server = irc.server()
	server.connect ( network, port, nick, ircname )
	for channel in channels:
		server.join ( channel )
	return server

server = server_object ( network, nick, name, port, ircname = name )

#jumps into infinite loop
irc.process_forever()
