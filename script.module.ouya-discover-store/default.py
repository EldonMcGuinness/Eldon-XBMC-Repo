import os

# Command to launch
cmd = '/system/bin/am start -n tv.ouya.console/.launcher.discover.DiscoverActivity -a android.intent.action.VIEW -eu ouya://launcher/discover'

if ( __name__ == "__main__" ):
    os.system(cmd.encode('utf-8'))