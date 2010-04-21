# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 23:46:10 2010

@author: jacob
"""

from visettings import Visettings
from window import Window
from scoreboard import Scoreboard
from gameboard import Gameboard
from minimap import Minimap
from plantinfo import Plantinfo
from legend import Legend
import curses

class VISMODE:
    PAUSE = 0
    PLAY = 1
    REWIND = 2

class Viscontrol( Window ):
    score = 0
    gameboard = 0
    plantInfo = 0
    minimap = 0
    
    def __init__(self, x, y, game):
        Window.__init__( self, x, y, 200, 2) 
        
        Visettings.Speed = -1
        
        if Visettings.AutoEnd :
            Visettings.CurrentMode = VISMODE.PLAY
        else:
            Visettings.CurrentMode = VISMODE.PAUSE
        
        Visettings.MaxX = game.states[0].boardX-1
        Visettings.MaxY = game.states[0].boardY-1
        
        Visettings.Player1Name = game.getName(0)
        Visettings.Player2Name = game.getName(0)
        
        Visettings.Game = game
        
        self.Window.erase()
        self.Window.refresh()
        
        self.moveWindow( x, Visettings.MaxY*2+4 )
        
        self.score = Scoreboard( x+Visettings.MaxX*2+5, y, 31, Visettings.MaxY*2+4 )
        self.gameboard = Gameboard( x, y, Visettings.MaxX*2+4, Visettings.MaxY*2+4 )
        self.plantInfo = Plantinfo( x+Visettings.MaxX*2+5+31, y, 32, Visettings.MaxY+1 )
        self.minimap = Minimap( x+Visettings.MaxX*2+5+31+30/2 - Visettings.MaxX/2, \
        Visettings.MaxY+1, \
        Visettings.MaxX+3, \
        Visettings.MaxY+3 )
        
        Visettings.CurX = 0
        Visettings.CurY = 0
        
        self.Window.erase()
        
    def updateMode(self, mode):
        Visettings.CurrentMode = mode
        if mode == VISMODE.PLAY or mode == VISMODE.REWIND:
            Visettings.Speed = Visettings.PlaySpeed
        elif mode == VISMODE.PAUSE:
            Visettings.Speed = -1
            
    
    def run( self ):
        if Visettings.AutoEnd and Visettings.Done:
            return 0
            
        if Visettings.FirstRun:
            self.update()
            Visettings.FirstRun = 0
            
        
        Visettings.Screen.timeout( Visettings.Speed )
        c = Visettings.Screen.getch()
       
        try:
            ch = curses.keyname( c )
        except:
            ch = c
        
        
        if ch == 'q':
            return 0
        elif ch == ' ' or ch == 'p':
            if Visettings.CurrentMode == VISMODE.PAUSE:
                self.updateMode( VISMODE.PLAY )
            else:
                self.updateMode( VISMODE.PAUSE )
        elif ch == 'r':
            self.updateMode( VISMODE.REWIND )
        elif ch == '.':
            self.updateMode( VISMODE.PAUSE )
            self.nextFrame()
        elif ch == ',':
            self.updateMode( VISMODE.PAUSE )
            self.prevFrame()
        elif ch == '=':
            Visettings.PlaySpeed -= 5
            if Visettings.PlaySpeed < 0:
                Visettings.PlaySpeed = 1
            self.updateMode( Visettings.CurrentMode )
        elif ch == '-':
            Visettings.PlaySpeed += 5
            self.updateMode( Visettings.CurrentMode )
        elif ch == 's':
            Visettings.FrameNumber = 0
        elif ch == 'e':
            Visettings.FrameNumber = len(Visettings.Game.states)-1
        elif c == curses.KEY_LEFT:
            Visettings.CurX -= 1
        elif c == curses.KEY_RIGHT:
            Visettings.CurX += 1
        elif c == curses.KEY_UP:
            Visettings.CurY -= 1
        elif c == curses.KEY_DOWN:
            Visettings.CurY += 1
        elif c == curses.KEY_MOUSE:
            k = 0
            
        if Visettings.CurrentMode == VISMODE.PLAY:
            self.nextFrame()
        elif Visettings.CurrentMode == VISMODE.REWIND:
            self.prevFrame()
            
        self.update()
        
        return 1
            
    def nextFrame( self ):
        Visettings.FrameNumber += 1
        if Visettings.FrameNumber >= len(Visettings.Game.states):
            Visettings.FrameNumber = len(Visettings.Game.states)-1
        
        
    def prevFrame( self ):
        Visettings.FrameNumber -= 1
        if Visettings.FrameNumber < 0:
            Visettings.FrameNumber = 0
        
    def update( self ):
        Window.update(self)
        self.Window.attrset( curses.color_pair( Legend.DEFAULT_COLOR ) )
        
        Visettings.Screen.refresh()
        
        # TODO: A bunch of attribute stuff is missing.
        
        Visettings.State = Visettings.Game.states[Visettings.FrameNumber];
        Visettings.Player1Score = Visettings.Game.states[Visettings.FrameNumber].player0Score
        Visettings.Player2Score = Visettings.Game.states[Visettings.FrameNumber].player1Score
        Visettings.Player1Light = Visettings.Game.states[Visettings.FrameNumber].player0Light
        Visettings.Player2Light = Visettings.Game.states[Visettings.FrameNumber].player1Light
        
        self.score.update()
        self.gameboard.newState()
        self.minimap.newState()
        self.plantInfo.update()
        
        offset = 50
        
        percent = float(Visettings.FrameNumber+1)/len(Visettings.Game.states)
        
        if percent > 1:
            percent = 1
        
        blocks = int((Visettings.MaxX*2+offset-10)*percent)
        
        for i in range(1, blocks+1):
            self.Window.addch( 0, i, curses.ACS_HLINE )
        for i in range( blocks+1, Visettings.MaxX*2+offset-9 ):
            self.Window.addch( 0, i, ' ' )
            
        self.Window.addch( 0, 0, curses.ACS_LLCORNER )
        self.Window.addch( 0, Visettings.MaxX*2+offset-9, curses.ACS_LRCORNER )
        
        if Visettings.CurrentMode == VISMODE.PAUSE:
            self.Window.addstr( 0, Visettings.MaxX*2+offset-7, "PAUSED      " )
        elif Visettings.CurrentMode == VISMODE.PLAY:
            self.Window.addstr( 0, Visettings.MaxX*2+offset-7, "PLAYING     " )
        elif Visettings.CurrentMode == VISMODE.REWIND:
            self.Window.addstr( 0, Visettings.MaxX*2+offset-7, "REWINDING   " )
            
        blue = 0
        red = 0
        width = 93
        
        red = Visettings.Player1Plants
        blue = Visettings.Player2Plants
        
        size = Visettings.MaxX * Visettings.MaxY

        rPercent = float(red)/size
        bPercent = float(blue)/size
        gPercent = float(1 - rPercent - bPercent)

        line = 2

        self.Window.attrset( curses.color_pair( Legend.PLAYER_1_PIECE_COLOR ) )
        self.Window.attron( curses.A_BOLD )
        self.Window.addch( 1, 1, curses.ACS_LLCORNER )
        self.Window.attrset( curses.color_pair( Legend.PLAYER_2_PIECE_COLOR ) )
        self.Window.attron( curses.A_BOLD )
        self.Window.addch( 1, 95, curses.ACS_LRCORNER )

        for i in range(0, width):
            if i+1 < rPercent*width:
                self.Window.attrset( curses.color_pair( Legend.PLAYER_1_PIECE_COLOR ) )
            elif i < (rPercent+gPercent)*width:
                self.Window.attrset( curses.color_pair( Legend.BACKGROUND_COLOR ) )
            else:
                self.Window.attrset( curses.color_pair( Legend.PLAYER_2_PIECE_COLOR ) )
            self.Window.attron( curses.A_BOLD )

            if i == width/2:
                self.Window.addch( 1, 2+i, '|' )
            else:
                self.Window.addch( 1, 2+i, curses.ACS_HLINE )

        self.Window.attroff( curses.A_BOLD )


        
        self.Window.refresh()
        Visettings.Screen.refresh()
