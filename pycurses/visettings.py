# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 17:37:37 2010

@author: jacob
"""

class Visettings:
    __shared_state = {}
    Screen = 0
    
    CurrentMode = 0
    Speed = 0
    PlaySpeed = 100
    
    FrameNumber = 0
    
    MaxX = 0
    MaxY = 0
    
    Player1Name = 0
    Player2Name = 0
    
    Player1Plants = 0
    Player2Plants = 0
    
    AutoEnd = 0
    
    CurX = 0
    CurY = 0
    
    Done = 0
    FirstRun = 1
    
    P1TextF = 1
    P1TextB = 0
    
    P2TextF = 4
    P2TextB = 0
    
    P1PieceF = 7
    P1PieceB = 1
    
    P2PieceF = 7
    P2PieceB = 4
    
    InstrF = 7
    InstrB = 0
    
    BackgroundF = 2
    BackgroundB = 0
    
    DefaultF = 7
    DefaultB = 0
    
    SelectionF = 0
    SelectionB = 6
    
    Game = 0
    State = 0
    
    
    def __init__(self):
        self.__dict__ = self.__shared_state
    
    
    
