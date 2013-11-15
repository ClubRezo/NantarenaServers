#!/usr/bin/env python
#encoding: utf-8

"""
Counter Strike Global Offensive Dedicated Server CLI

Handle the launch of CSGO server with a powerful set of options

@author:  Quentin Lebourgeois <quentin.lebourgeois@gmail.com>
@date:    November 2013
"""

import sys, os, argparse, subprocess, screenutils

# program information
__program__ = "csgo"
__version__ = "1 (dev)"
__description__ = "CSGO Dedicated Server launcher"

# some constants
SV_EXECUTABLE = "./srcds_run"
SV_ROOT_DIR = "/srv/csgo/"
SV_SCREEN_NAME = "csgo"
SV_AUTHKEY = "8EA5D60A192C38B72D51386A776E4EEB"

# default parameters
SV_IP = "0.0.0.0"
SV_HOSTNAME = "Counter Strike Global Offensive Server"
SV_PORT = 27015
SV_TICKRATE = 128
SV_PLAYERS = 12

# server maps config
SV_MAPGROUP = 193593299
SV_STARTMAP = 125438255

# tv config
TV_PORT = 27020

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
    Argument Parser made for the CSGO DS Launcher
    """
    
    def __init__(self):
        super(LauncherArgumentParser, self).__init__()
        
        # command line description (version number given too)
        self.description = "%s Version %s" % (__description__, __version__)
        
        self.add_argument("sv_game_mode", choices=["casual", "competitive", "deathmatch"],
            help="game mode for the dedicated server", default="casual")
        self.add_argument("-p", "--port", default=SV_PORT, type=int, dest="sv_port", 
            help="listen port (default: %s)" % SV_PORT)
        self.add_argument("-H", "--hostname", default=SV_HOSTNAME, dest="sv_hostname", 
            help="server hostname (default: %s)" % SV_HOSTNAME)
        self.add_argument("--ip", dest="sv_ip", default=SV_IP,
            help="listen IP (default: %s)" % SV_IP)
        self.add_argument("-t", "--tickrate", default=SV_TICKRATE, type=int, dest="sv_tickrate", 
            help="server tickrate (default: %s)" % SV_TICKRATE)
        self.add_argument("--players", default=SV_PLAYERS, type=int, dest="sv_players", 
            help="server max players (default: %s)" % SV_PLAYERS)
        self.add_argument("--mapgroup", default=SV_MAPGROUP, type=int, dest="sv_mapgroup", 
            help="server map group (default: %s)" % SV_MAPGROUP)
        self.add_argument("--startmap", default=SV_STARTMAP, type=int, dest="sv_startmap", 
            help="server start map (default: %s)" % SV_STARTMAP)
        self.add_argument("--authkey", default=SV_AUTHKEY, dest="sv_authkey", 
            help="workshop auth key (default: %s)" % SV_AUTHKEY)
        self.add_argument("--tvport", default=TV_PORT, type=int, dest="tv_port", 
            help="tv port (default: %s)" % TV_PORT)
        self.add_argument("-d", "--daemon", action="store_true", dest="sv_daemon", 
            help="daemonize server")

def get_game_mode(mode):
    """
    Determine the approriate game mode
    """

    game_mode = (0, 0)

    if mode == "competitive":
        game_mode = (0, 1)
    elif mode == "deathmatch":
        game_mode = (1, 2)
    
    return game_mode

def start_server(args):
    """
    Start a new instance of a CSGO Dedicated Server
    """

    # get game mode
    game_type, game_mode = get_game_mode(args.sv_game_mode)

    # move to the root server dir
    os.chdir(SV_ROOT_DIR)

    cmd_core    = "%s -game csgo -console -usercon" % SV_EXECUTABLE
    cmd_server  = "-tickrate %i +hostname %s" % (args.sv_tickrate, args.sv_hostname)
    cmd_network = "-ip %s -port %i" % (args.sv_ip, args.sv_port)
    cmd_game    = "+game_type %i +game_mode %i -maxplayers_override %i" % (game_type, game_mode, args.sv_players)
    cmd_maps    = "+host_workshop_collection %i +workshop_start_map %i -authkey %s" % (args.sv_mapgroup, args.sv_startmap, args.sv_authkey)
    cmd_tv      = "+tv_port %i" % args.tv_port

    cmdline = "%s %s %s %s %s %s" % (cmd_core, cmd_network, cmd_server, cmd_game, cmd_maps, cmd_tv)

    # launch the dedicated server
    if args.sv_daemon:
        # init a new screen
        screen = screenutils.Screen(SV_SCREEN_NAME, initialize=True)

        # start a new csgo ds
        screen.send_commands(cmdline)

        print "[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC  + " ] " + "Launch CSGO Dedicated Server listening on %s:%s" % (args.sv_ip, args.sv_port)
    else:
        os.system(cmdline)

         # print the success message
        print "[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC  + " ] " + "Server terminated with success"

def main():
    """
    Main function for CSGO DS Launcher
    """

    args = LauncherArgumentParser().parse_args()

    try:
        start_server(args)
    except Exception as e:
        print "[" + bcolors.FAIL + "fail" + bcolors.ENDC  + "] " + "Error while launching CSGO Dedicated Server" + " (error: %s)" % e ; return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
