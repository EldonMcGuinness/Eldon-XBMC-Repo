#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmcgui, xbmcplugin, xbmcaddon
import urllib, urllib2, urlparse, re

# Add our resources/lib to the python path
try:
	current_dir = os.path.dirname(os.path.abspath(__file__))
except:
	current_dir = os.getcwd()
sys.path.append(os.path.join(current_dir, 'resources', 'lib'))

import youtube

addon = xbmcaddon.Addon('plugin.video.gracelink-kindergarten')

# Addon Constants
__addon__	  = xbmcaddon.Addon()
__author__	 = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__		= __addon__.getAddonInfo('path')
__version__	= __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

print('Args \n\n{0}\n\n'.format(str(args)))

xbmcplugin.setContent(addon_handle, 'episodes')

playlists =	[
	{	'title':'Kindergarten Class',
	 	'lists':[
			{'title':'Kindergarten Year A Quarter 1','id':'PLkFyfqehc4MqiOLhHl-TBY2Insri9KsrX'},
			{'title':'Kindergarten Year A Quarter 2','id':'PLkFyfqehc4MrfyIJpsxBNbw0RnvT_A-9D'},
			{'title':'Kindergarten Year A Quarter 3','id':'PLkFyfqehc4MoqTfgh4BL6_Sc2ubLNReNi'},
			{'title':'Kindergarten Year A Quarter 4','id':'PLkFyfqehc4Mq8LFO38k7BlH5JFNQy6AKo'},
			{'title':'Kindergarten Year B Quarter 1','id':'PLkFyfqehc4MqmeWW539aTLIvCI3e8Krha'},
			{'title':'Kindergarten Year B Quarter 2','id':'PLkFyfqehc4Mqf4z1ATsZ6Crd-WJY2W50f'},
			{'title':'Kindergarten Year B Quarter 3','id':'PLkFyfqehc4MotyxUvT27ziFGJrqqpQdj0'},
			{'title':'Kindergarten Year B Quarter 4','id':'PLkFyfqehc4MqhlgTZf8K7WaJi0juXZ_IK'}
		]
	},
	{	'title':'Primary Class',
		'lists':[
			{'title':'Primary Year B Quarter 2','id':'PLkFyfqehc4MofndO_18NnKT38DvR5l3FW'},
			{'title':'Primary Year B Quarter 3','id':'PLkFyfqehc4MrEfbkSfsTgoc0a_C4xSOYO'},
			{'title':'Primary Year B Quarter 4','id':'PLkFyfqehc4MpqymqF6JZcqTHuEBH38GJ6'},
			{'title':'Primary Year C Quarter 1','id':'PLkFyfqehc4Mow8feqV_NCBGILho4UHXFL'},
			{'title':'Primary Year C Quarter 2','id':'PLkFyfqehc4MrTpxhsg8xjVOlZi8KLTguw'},
			{'title':'Primary Year C Quarter 3','id':'PLkFyfqehc4MoGZLQJb8-_k-PICN9mBKfk'},
			{'title':'Primary Year C Quarter 4','id':'PLkFyfqehc4MpaCfc7yb5Z_rvXCUzxzYBg'},
			{'title':'Primary Year D Quarter 1','id':'PLkFyfqehc4MpAI6FQYzSOO8_QbYZ4k6Bq'},
			{'title':'Primary Year D Quarter 2','id':'PLkFyfqehc4Mr-0Qf5M_y1gJPwK7p2iNtb'},
			{'title':'Primary Year D Quarter 3','id':'PLQ0Sfw7dzlJzdxEoL3CBsBk_xtpulA_fS'}
		]
	}
]

# Default icon for directories
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')

# The current mode of the view
# None shows the main folders
# Folder shows the contents of a feed
mode = args.get('mode', None)
playlistId = args.get('playlistId', None)

# In case we get a list, strip it
if type(playlistId) is list:
	playlistId = playlistId[0] 

if type(mode) is list:
	mode = mode[0] 


def __buildUrl(query):
	return base_url + '?' + urllib.urlencode(query)

def cleanTitle(title):
	title = re.sub(ur'.*?(\d+)\s?\:?\s?\"(.+)\"$',ur'Lesson \1: \2',title)
	title = re.sub(ur'.*L(\d+)\s?\:?\s?(.+)$',ur'Lesson \1: \2',title)
	return title

if (__name__ == "__main__"):
	print('Addon Started')

	#Create the base folders for Primary and Kindergarten

	if mode is None:
		index = 0
		for item in playlists:
			print('Added Folder [{0}|{1}]'.format(item['title'],index))
			url = __buildUrl({'mode':'folder','foldername':item['title'],'playlistId':index})
			li = xbmcgui.ListItem(label=item['title'], iconImage=icon, thumbnailImage=icon)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
			index+=1
	elif mode == 'folder':
		for item in playlists[int(playlistId)]['lists']:
			print('Added Folder [{0}]'.format(item['id']))
			url = __buildUrl({'mode':'section','foldername':item['title'],'playlistId':item['id']})
			li = xbmcgui.ListItem(label=item['title'], iconImage=icon, thumbnailImage=icon)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	else:
		print('Fetching playlist: [{0}]'.format(playlistId))
		playlist = youtube.playlistBuilder(playlistId)
		for item in playlist.items:
			video = youtube.videoFinder(item['videoId']).getBestQuality()
			print 'Thumbnail [{0}]'.format(video['img'])
			li = xbmcgui.ListItem(
				label=cleanTitle(item['title']),
				thumbnailImage=video['img'],
				iconImage=video['img']
			)
			xbmcplugin.addDirectoryItem(
				handle=addon_handle, 
				url=video['url'],
				listitem=li
			)
			video = None

	xbmcplugin.endOfDirectory(addon_handle)
