# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:00:30 2010

@author: jacob
"""

import curses
import libparsermodule as pm
from legend import Legend
from visettings import Visettings
from window import Window


class Plantinfo(Window):
    def __init__(self, x, y, width, height ):
        Window.__init__(self, x, y, width, height )
    
    def printInfo(self, n, str):
        self.Window.addstr( n, 2, str + "      " )
        n+=1
        return n

    def update(self):
        self.Window.erase()
        self.Window.box(0,0 )
        self.Window.attron( curses.color_pair( Legend.DEFAULT_COLOR ) )
        
        if Visettings.Plant:
            i = 3
            if not Visettings.AutoEnd:
                self.Window.addstr( 1, 2, "Plant Info" )
                info = ["Health: %d" % (Visettings.Plant.health ),
                "Roof Level: %d" % (Visettings.Plant.rootLevel ),
                "Leaf Level: %d" % (Visettings.Plant.leafLevel ),
                "Flower Level: %d" % (Visettings.Plant.flowerLevel ),
                "Root LvlUp: %d" % (Visettings.Plant.rootLevelUp ),
                "Leaf LvlUp: %d" % (Visettings.Plant.leafLevelUp ),
                "Flower LvlUp: %d" % (Visettings.Plant.flowerLevelUp )
                ]


                for k in info:
                    i = self.printInfo( i, k )
                # Print Stuff
            else:
                pass
                # LIB CURL TOP 3 SEEDS
                
            # TALKING: Need to fix this error
            for j in pm.getAnims(Visettings.State):
                if j.type == 7:
                    if Visettings.Plant.objectID == j.plantID:
                        w = 0
                        msg = pm.getTalk( j )
                        nLine = 0

                        for k in range( 0, 28 ):
                            if msg[k] == '\n':
                                nLine = 1

                        l = 0

                        while len( msg )-w > 28 or nLine:
                            l = w+28
                            nLine = 0

                            for k in range( w, l ):
                                if msg[k] == '\n':
                                    l = k
                                    break                          
                            self.Window.addstr( i, 2, msg[w:l] )
                            w = l+1
                            i+=1

                            for k in range( w, w+28 ):
                                if k < len(msg) and msg[k] == '\n':
                                    nLine = 1
                                    break
        
                        self.Window.addstr( i, 2, msg[w:] )
                        i+=1
        else:
            if not Visettings.AutoEnd:
                self.Window.addstr( 1, 2, "Empty" )
            else:
                pass
        
        self.Window.box( 0, 0 )
        self.Window.refresh()
