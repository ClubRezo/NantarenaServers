#!/usr/bin/env python
#encoding: utf-8

"""
eBot Server Launcher

Handle the launch of eBot daemonized or not

@author:  Quentin Lebourgeois <quentin.lebourgeois@gmail.com>
@date:    November 2013
"""

import sys, os, argparse, screenutils

# program information
__program__ = "ebot"
__version__ = "1 (dev)"
__description__ = "eBot Launcher"

# some constants
BOT_ROOT_DIR = "/home/nantarena/ebotv3"
BOT_SCREEN_NAME = "ebot"
BOT_DAEMON = False

class bcolors:
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class LauncherArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser made for eBot launcher
    """
    
    def __init__(self):
        super(LauncherArgumentParser, self).__init__()
        
        # command line description (version number given too)
        self.description = "%s Version %s" % (__description__, __version__)

        self.add_argument("-d", "--daemon", action="store_true", dest="bot_daemon", 
            help="launch eBot as a daemon")

def main():
    """
    Main function for eBot launcher
    """

    args = LauncherArgumentParser().parse_args()

    try:
        os.chdir(BOT_ROOT_DIR)

        if args.bot_daemon:
            # init a new screen
            screen = screenutils.Screen(BOT_SCREEN_NAME, initialize=True)

            # send ebot start
            screen.send_commands("php bootstrap.php")

            print "[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC  + " ] " + "Launching eBot server"
        else:
            os.system("php bootstrap.php")
        
            print "[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC  + " ] " + "Terminating eBot server instance"
    except Exception as e:
        print "[" + bcolors.FAIL + "fail" + bcolors.ENDC  + "] " + "Error while lauching eBot server" + " (error: %s)" % e ; return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
