#!/usr/bin/env python3

import os

import pygame as pg

from ResourceManager import ResourceManager
from Component import Component
from Actions import Actions

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
        # Initilized Pygame Library
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None

        # Sets up Window/Screen Display
        self.winstyle = FULLSCREEN 
        self.bestdepth = pg.display.mode_ok(SCREENRECT.size, self.winstyle, 32)
        self.screen = pg.display.set_mode(SCREENRECT.size, self.winstyle, self.bestdepth)
        pg.display.set_caption("Depth")

        # Stateful variables about mouse movement & IO events
        self.mouse_rel = pg.mouse.get_rel()
        self.events = []

        self.resources = ResourceManager()

        # Initialize Containers/Components/UI
        self.main_menu = Component(SCREENRECT.x, SCREENRECT.y, SCREENRECT.w/2, SCREENRECT.h)
        
        self.current_component = self.main_menu
    
    '''
    Main Game Loop
    '''
    def loop(self):
        running = True
        clock = pg.time.Clock()
        while True:
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    exit(1)
            # Get the relative movement (velocity vector) of the mouse position per frame
            self.mouse_rel = pg.mouse.get_rel()            

            # Main Root update 
            self.current_component.update(self)
            self.current_component.render(self)

            # Limit Game to 60 FPS
            clock.tick(60)


    '''
    Starts Depth
    '''
    def start(self):
        self.loop()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
