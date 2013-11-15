#!/usr/bin/env python
#encoding: utf-8

"""
Manager for Valve Dedicated Server

Handle Valve Dedicated Server launching, able to launch several servers in parallel

@author:  Quentin Lebourgeois <quentin.lebourgeois@gmail.com>
@date:    November 2013
"""

import sys, argparse

# program information
__program__ = "dedicated"
__version__ = "1 (dev)"
__description__ = "Valve Dedicated Server Launcher"

# default parameters
DE_DEFAULT_GAME = "csgo"
DE_INSTANCES = 1

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
    Argument Parser made for the Dedicated Server Launcher
    """
    
    def __init__(self):
        super(LauncherArgumentParser, self).__init__()
        
        # command line description (version number given too)
        self.description = "%s Version %s" % (__description__, __version__)
        
        self.add_argument("game", choices=["csgo"],
            help="game to launch", default="casual")
        self.add_argument("-N", "--instances", default=DE_INSTANCES, type=int, dest="de_instances", 
            help="number of instances (default: %i)" % DE_INSTANCES)

def launch_csgo(options):
    """
    Launch CSGO server with options
    """



def main():
    """
    Main function for CSGO DS Launcher
    """

    args = LauncherArgumentParser().parse_args()

    try:
        start_server(args)
    except Exception as e:
        print "[" + bcolors.FAIL + "fail" + bcolors.ENDC  + "] " + "Error while launching dedicated server" + " (error: %s)" % e ; return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
