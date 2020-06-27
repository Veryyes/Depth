#!/usr/bin/env python3

import os
import math

import pygame as pg

from Component import Component
from Actions import Actions
from MainMenu import MainMenu
from SongPlayer import SongPlayer
from SongBuilder import SongBuilder
from Song import Song

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
        self.screen_rect = SCREENRECT
        pg.display.set_caption("Depth")
        
        # Stateful variables about mouse movement & IO events
        self.mouse_rel = pg.mouse.get_rel()
        self.events = []

        # Initialize Containers/Components/UI
        self.main_menu = MainMenu(self)

        self.song_player = SongPlayer(self, current_song = "Niji no Kanata ni.ogg")
        
        self.song_builder = SongBuilder(self)

        self.current_component = self.main_menu
    
    def change_to_main_menu(self):
        self.current_component = self.main_menu

    def change_to_song_player(self):
        self.current_component = self.song_player

    def change_to_song_builder(self):
        self.current_component = self.song_builder

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
                    self.close()
            # Get the relative movement (velocity vector) of the mouse position per frame
            self.mouse_rel = pg.mouse.get_rel()            

            # Main Root update 
            self.current_component.update(self)
            self.current_component.render(self)

            pg.display.update()
            # Limit Game to 60 FPS
            clock.tick(60)

    def screen_diagonal(self):
        w = self.screen_rect.w
        h = self.screen_rect.h
        return math.sqrt(w*w + h*h)

    def close(self):
        exit(0)

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
