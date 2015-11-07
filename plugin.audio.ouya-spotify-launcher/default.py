import xbmc, xbmcaddon

addon = xbmcaddon.Addon(id='plugin.audio.com.spotify.music')

# Addon Constants
__addon__      = xbmcaddon.Addon()
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

if ( __name__ == "__main__" ):
	xbmc.executebuiltin('XBMC.StartAndroidActivity("com.spotify.music")')
