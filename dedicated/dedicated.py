#!/usr/bin/env python
#encoding: utf-8

"""
Manager for Valve Dedicated Server

Handle Valve Dedicated Server launching, able to launch several servers in parallel

@author:  Quentin Lebourgeois <quentin.lebourgeois@gmail.com>
@date:    November 2013
"""

import os, sys, argparse, time, importlib

# program information
__program__ = "dedicated"
__version__ = "1 (dev)"
__description__ = "Valve Dedicated Server Launcher"

# default parameters
DE_SCRIPTS_DIR = "/home/nantarena/servers/dedicated"
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
        
        self.add_argument("game", choices=["csgo"], help="game to launch", default="casual")
        self.add_argument("-N", "--instances", default=DE_INSTANCES, type=int, dest="de_instances", 
            help="number of instances (default: %i)" % DE_INSTANCES)
        self.add_argument("-O", "--options", dest="de_options", nargs=argparse.REMAINDER,
            help="server options")

def launch(args):
    """
    Launch a dedicated server with options
    """

    # goto the scripts dir
    os.chdir(DE_SCRIPTS_DIR)

    # automatic -d option append
    args.de_options.append("--daemon")

    servers_list = []
    port = 27015

    if args.game == "csgo":
        for i in range(0, args.de_instances):
            # specify a custom screen name
            args.de_options.extend(["--screen-name", "%s.%i" % (args.game, port)])
            # append server to servers list
            servers_list.append("%s:%i" % (args.game, port))

            launch_csgo(args, port)
            port = port + 10 ; time.sleep(2)

    return servers_list

def launch_csgo(args, port):
    """
    Launch CSGO Dedicated Server as a daemon
    """

    # force port
    args.de_options.extend(["-p", port])

    # launch csgo ds
    result = os.system("python %s.py %s" % (args.game, " ".join(str(x) for x in args.de_options)))

    if result != 0:
        raise Exception("Unable to launch dedicated server on port %i" % port)

def main():
    """
    Main function for CSGO DS Launcher
    """

    args = LauncherArgumentParser().parse_args()

    try:
        servers_list = launch(args)

        # clear console
        os.system("clear")

        for server in servers_list:
            print "[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC + " ] " + "Launched 1 server %s" % (server)
    except Exception as e:
        print "[" + bcolors.FAIL + "fail" + bcolors.ENDC + "] " + "Error while launching dedicated server" + " (error: %s)" % e ; return 1

    print "[" + bcolors.BOLD + "info" + bcolors.ENDC + "] " + "Launched %i server(s) of %s" % (args.de_instances, args.game)

    return 0

if __name__ == "__main__":
    sys.exit(main())
