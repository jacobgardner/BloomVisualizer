# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 00:49:41 2010

@author: jacob
"""

import curses
from legend import Legend
from window import Window
from visettings import Visettings

        
class Scoreboard( Window ):
    def __init__(self, x, y, width, height):
        Window.__init__( self, x, y, width, height) 

    def printLine( self, n, str ):
        self.Window.addstr( n, 3, str )
        n+=1
        return n

    def update( self ):
        Window.update( self )
        
        line = 1
        
        red = 0
        blue = 0
        
        highestLevel = [0,0]
        for i in Visettings.State.plants:
            if i.ownerID: 
                blue += 1
            else:
                red += 1
                
            if i.rootLevel + i.leafLevel + i.flowerLevel > highestLevel[i.ownerID]:
                highestLevel[i.ownerID] = i.rootLevel + i.leafLevel + i.flowerLevel 
                
        self.Window.addstr( line, 2, "Turn: %d     " % (Visettings.FrameNumber) )
        line+=1
        
        self.Window.attrset( curses.color_pair( Legend.PLAYER_1_COLOR  ) )
        self.Window.addstr( line, 2, "----------------------------" )
        line+=1
        line = self.printLine( line, Visettings.Player1Name )
        self.Window.addstr( line, 2, "----------------------------" )
        line+=1
        line = self.printLine( line, "Score: %d     " % (Visettings.Player1Score) )
        line = self.printLine( line, "Light: %d     " % (Visettings.Player1Light) )
        line = self.printLine( line, "Plants: %d     " % (red) )
        
        self.Window.attrset( curses.color_pair( Legend.PLAYER_2_COLOR  ) )
        line+=2
        self.Window.addstr( line, 2, "----------------------------" )
        line+=1
        line = self.printLine( line, Visettings.Player2Name )
        self.Window.addstr( line, 2, "----------------------------" )
        line+=1
        line = self.printLine( line, "Score: %d     " % (Visettings.Player2Score) )
        line = self.printLine( line, "Light: %d     " % (Visettings.Player2Light) )
        line = self.printLine( line, "Plants: %d     " % (blue) )
        line = self.printLine( line, "Plant Level: %d     " % (highestLevel[1]) )
        
        self.Window.attrset( curses.color_pair( Legend.INSTRUCTIONS ) )
        
        line = Visettings.MaxY*2-12
        
        Visettings.Player1Plants = red
        Visettings.Player2Plants = blue
        
        instructions = [
        "Visualizer Usage: ",
        "Q     | Quit",
        "P     | Pause/Play",
        "R     | Rewind",
        "+     | Increase Speed",
        "-     | Decrease Speed",
        ">     | Go ahead one frame",
        "<     | Go back one frame",
        "E     | Go to last frame ",
        "S     | Go to first frame",
        "Left  | Move Cursor Left",
        "Right | Move Cursor Right",
        "Up    | Move Cursor Up",
        "Down  | Move Cursor Down"]
        
        for k in instructions:
            line = self.printLine( line, k )
        
        self.Window.refresh()
        Visettings.Screen.refresh()
