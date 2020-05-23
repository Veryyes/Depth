#!/usr/bin/env python3

import os

import pygame as pg
from ResourceManager import ResourceManager

FULLSCREEN = 0
SCREENRECT = pg.Rect(0, 0, 640, 480)

'''
Represention of the Game itself.
Game should store all the related game context data as it should be the first parameter (besides self) in many of the other objects used 
'''
class Game:
    '''
    Initalizes Depth.
    '''
    def __init__(self):
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None

        self.winstyle = FULLSCREEN
        self.bestdepth = pg.display.mode_ok(SCREENRECT.size, self.winstyle, 32)
        self.screen = pg.display.set_mode(SCREENRECT.size, self.winstyle, self.bestdepth)

        self.resources = ResourceManager()
    
    '''
    Main Game Loop
    '''
    def loop(self):
        pass

    '''
    Starts Depth
    '''
    def start(self):
        self.loop()


def main():
    game = Game()
    game.start()


if __name__ = "__main__":
    main()
