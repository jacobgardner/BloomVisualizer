# -*- coding: utf-8 -*-


from window import Window
from visettings import Visettings
import curses
from legend import Legend

class Minimap(Window):
    def __init__(self, x, y, width, height):
        Window.__init__(self, x, y, width, height )        

    def newState(self):
        for i in range(0, Visettings.BoardX):
            for j in range( 0, Visettings.BoardY ):
                self.Window.attron( curses.color_pair( Legend.BACKGROUND_COLOR ) )
                self.Window.addch(1+j, 1+i, curses.ACS_CKBOARD )
                self.Window.attroff( curses.color_pair( Legend.BACKGROUND_COLOR ) )
                    
        plant = 0
        dead = 0
        
        if Visettings.AutoEnd:
            pass
            
        for i in Visettings.State.plants:
            self.Window.attron( curses.color_pair( Legend.PLAYER_1_PIECE_COLOR+i.ownerID ) )
                
            ch = ' ' 
                
            self.Window.addch( i.y+1, i.x+1, ch )
            
        Window.update(self)
        
        # TODO: WIN ANIMATION

   
