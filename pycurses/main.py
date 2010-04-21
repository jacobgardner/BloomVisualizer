
import sys
import curses

from visettings import Visettings
from viscontrol import Viscontrol

import libparsermodule as pm


def main(argv):
        
    game = pm.Game()
    
    if len(argv) < 2:
        print "Must Give Log File"
        return 0
    
    if not pm.parseFile( game, argv[1] ):
        print "Game Log " + argv[1] + " Not Found!"
        return 0
        
    
    print len( game.states )
    
    # Initialize Ncurses
    Visettings.Screen = curses.initscr()
    curses.cbreak()
    curses.noecho()
    
    Visettings.Screen.keypad( 1 )
    
    curses.mousemask( curses.ALL_MOUSE_EVENTS )
    
    # Allow Color
    curses.start_color()
    
    # Start VISCONTROL
    vc = Viscontrol( 0, 0, game )
    
    # Run the loop
    while 1:
        if not vc.run() :
            break
    
    # Clean up Ncurses
    curses.endwin()
    
main(sys.argv)