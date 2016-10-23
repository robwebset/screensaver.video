# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcaddon

if sys.version_info >= (2, 7):
    import json
else:
    import simplejson as json

# Import the common settings
from resources.lib.settings import log
from resources.lib.settings import Settings

ADDON = xbmcaddon.Addon(id='screensaver.video')
CWD = ADDON.getAddonInfo('path').decode("utf-8")


##################################
# Main of the TvTunes Service
##################################
if __name__ == '__main__':
    log("VideoScreensaverService: Startup checks")

    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "params": { "addonid": "repository.robwebset", "properties": ["enabled", "broken", "name", "author"]  }, "id": 1}')
    json_response = json.loads(json_query)

    displayNotice = True
    if ("result" in json_response) and ('addon' in json_response['result']):
        addonItem = json_response['result']['addon']
        if (addonItem['enabled'] is True) and (addonItem['broken'] is False) and (addonItem['type'] == 'xbmc.addon.repository') and (addonItem['addonid'] == 'repository.robwebset') and (addonItem['author'] == 'robwebset'):
            displayNotice = False

            # Check if the settings mean we want to reset the volume on startup
            startupVol = Settings.getStartupVolume()

            if startupVol < 0:
                log("VideoScreensaverService: No Volume Change Required")
            else:
                log("VideoScreensaverService: Setting volume to %s" % startupVol)
                xbmc.executebuiltin('SetVolume(%d)' % startupVol, True)

            # Make sure that the settings have been updated correctly
            Settings.cleanAddonSettings()

            # Check if we should start the screensaver video on startup
            if Settings.isLaunchOnStartup():
                log("VideoScreensaverService: Launching screensaver video on startup")
                xbmc.executebuiltin('RunScript(%s)' % (os.path.join(CWD, "screensaver.py")))

    if displayNotice:
        xbmc.executebuiltin('Notification("robwebset Repository Required","github.com/robwebset/repository.robwebset",10000,%s)' % ADDON.getAddonInfo('icon'))
