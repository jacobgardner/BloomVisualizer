# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 01:28:14 2010

@author: jacob
"""

import curses
from legend import Legend
from window import Window
from visettings import Visettings

class Gameboard( Window ):
    def __init__(self, x, y, width, height ):
        Window.__init__(self, x, y, width, height )
        
        Visettings.BoardX = (width-2)/2
        Visettings.BoardY = (height-2)/2
        
        self.setupPieces()
        
    def setupPieces(self):
        curses.init_pair( 18, Visettings.SelectionF, Visettings.SelectionB )
        
        curses.init_pair( Legend.PLAYER_1_COLOR, Visettings.P1TextF, Visettings.P1TextB )
        curses.init_pair( Legend.PLAYER_2_COLOR, Visettings.P2TextF, Visettings.P2TextB )
        
        curses.init_pair( Legend.PLAYER_1_PIECE_COLOR, Visettings.P1PieceF, Visettings.P1PieceB )
        curses.init_pair( Legend.PLAYER_2_PIECE_COLOR, Visettings.P2PieceF, Visettings.P2PieceB )
        
        curses.init_pair( Legend.INSTRUCTIONS, Visettings.InstrF, Visettings.InstrB )
        curses.init_pair( Legend.BACKGROUND_COLOR, Visettings.BackgroundF, Visettings.BackgroundB )
        
        curses.init_pair( Legend.DEFAULT_COLOR, Visettings.DefaultF, Visettings.DefaultB )
        
    def newState(self):
        
        if Visettings.CurX < 0:
            Visettings.CurX = 0
        if Visettings.CurX > (self.Width-3)/2:
            Visettings.CurX = (self.Width-3)/2
        
        #self.Window.addstr(2, 2, "STRING STRING STRING STRING STRING STRING STRING STRING STRING" )
        
        for i in range(0, Visettings.BoardX):
            for j in range( 0, Visettings.BoardY ):
                if Visettings.CurX == i and \
                Visettings.CurY == j and \
                not Visettings.AutoEnd:
                    self.Window.attron( curses.color_pair( 18 ) )
                else:
                    self.Window.attron( curses.color_pair( Legend.BACKGROUND_COLOR ) )
                    
                
                self.Window.addch(1+j*2, 1+i*2, curses.ACS_CKBOARD )
                self.Window.addch(1+j*2, 2+i*2, curses.ACS_CKBOARD )
                self.Window.addch(2+j*2, 1+i*2, curses.ACS_CKBOARD )
                self.Window.addch(2+j*2, 2+i*2, curses.ACS_CKBOARD )
                
                if Visettings.CurX == i and \
                Visettings.CurY == j and \
                not Visettings.AutoEnd:
                    self.Window.attroff( curses.color_pair( 18 ) )
                else:
                    self.Window.attroff( curses.color_pair( Legend.BACKGROUND_COLOR ) )
                    
        plant = 0
 
        if Visettings.AutoEnd:
            pass
        
        for i in Visettings.State.plants:
            if i.x == Visettings.CurX and i.y == Visettings.CurY \
            and not Visettings.AutoEnd:
                self.Window.attron( curses.color_pair( 18 ) )
                Visettings.Plant = i
                plant = 1
            else:
                self.Window.attron( curses.color_pair( Legend.PLAYER_1_PIECE_COLOR+i.ownerID ) )
                
            ch = 0
            dead = 0    
            
            if i.health >= 20:
                ch = curses.ACS_S1
            elif i.health >= 15:
                ch = curses.ACS_S3
            elif i.health >= 10:
                ch = curses.ACS_S7
            elif i.health > 0:
                ch = '_'
            else:
                ch = '\\'
                dead = 1
                
            self.Window.attron( curses.A_BOLD )
            self.Window.addch( i.y*2+2, i.x*2+2, ch )
            
            if not dead:
                self.Window.attroff( curses.A_BOLD )
            
            if i.flower and not dead:
                ch = 'F'
            elif dead:
                ch = '\\'
            else:
                ch = ' '
            
            self.Window.addch( i.y*2+1, i.x*2+1, ch )
            
            if i.root and not dead:
                ch = 'R'
            elif dead:
                ch = '/'
            else:
                ch = ' '
            
            self.Window.addch( i.y*2+2, i.x*2+1, ch )

            if i.leaf and not dead:
                ch = 'L'
            elif dead:
                ch = '/'
            else:
                ch = ' '
            
            self.Window.addch( i.y*2+1, i.x*2+2, ch )
            
            if dead:
                self.Window.attroff( curses.A_BOLD )
            
            if i.x == Visettings.CurX and i.y == Visettings.CurY \
            and not Visettings.AutoEnd:
                self.Window.attroff( curses.color_pair( 18 ) )
            else:
                self.Window.attron( curses.color_pair( Legend.PLAYER_1_PIECE_COLOR+i.ownerID ) )
        
        if not plant:
            Visettings.Plant = 0            
        
        Window.update(self)
        
        # TODO: WIN ANIMATION

