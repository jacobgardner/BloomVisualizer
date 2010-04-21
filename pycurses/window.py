# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 22:10:26 2010

@author: jacob
"""

import curses
from visettings import Visettings

class Window:
    Window = 0
    X = 0
    Y = 0 
    Width = 10
    Height = 10
    
    def __init__(self, x, y, width, height ):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.createWindow()
        self.Window.refresh()        
        
    def createWindow(self):
        Visettings.Screen.refresh()
        self.Window = curses.newwin( self.Height, self.Width, self.Y, self.X )
        self.Window.box()
        self.Window.refresh()
    
    def deleteWindow(self):
        self.Window.erase()
        self.Window.attrset( 0 )
        self.Window.refresh()
        
    def moveWindow( self, x, y ):
        self.deleteWindow()
        self.X = x
        self.Y = y
        self.createWindow()
    
    def resizeWindow( self, width, height ):
        self.deleteWindow()
        self.Width = width
        self.Height = height
        self.createWindow()
        
    def update( self ):
        self.Window.refresh()
