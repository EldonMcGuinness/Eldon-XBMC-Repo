#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, xbmcgui, xbmcplugin, xbmcaddon
import urllib2, re
import xml.etree.ElementTree as ET

addon = xbmcaddon.Addon(id='plugin.video.gracelink-kindergarten')

# Addon Constants
__addon__      = xbmcaddon.Addon()
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

gracelinkXmlVideo = 'http://feeds.feedburner.com/KindergartenAnimation?format=xml'
gracelinkXmlAudio = 'http://feeds.feedburner.com/gracelink/KinAu?format=xml'
icon = 'https://raw.githubusercontent.com/EldonMcGuinness/Eldon-XBMC-Repo/stable/plugin.video.gracelink-kindergarten/icon.png'


def _getVideoInfo():
	global icon
	webData = urllib2.urlopen(gracelinkXmlVideo).read()
	webData = re.sub(r'feedburner\:',r'', webData)
	xmlRoot = ET.fromstring(webData)
	
	# (videoURL, Title, Description, Thumbnail)
	listItems = []
	channel = xmlRoot.find('channel')
	for video in channel.findall('item'):
		listItem = (video.find('origEnclosureLink').text, video.find('title').text, icon)
		listItems.append(listItem)

	return listItems
		
if (__name__ == "__main__"):
	print('Addon Started')

	listItems = _getVideoInfo()
	for listItem in listItems:
		li = xbmcgui.ListItem(label=listItem[1], iconImage=listItem[2])
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=listItem[0], listitem=li)

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
