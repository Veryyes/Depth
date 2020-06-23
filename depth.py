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
        self.main_menu = Component(SCREENRECT.x, SCREENRECT.y, SCREENRECT.w, SCREENRECT.h)
        mm = self.main_menu
        mm.image = self.resources.get_image("mm_back.png")
        mm.set_font("broadway")
        mm.text = "Depth"

        mm_exit_btn = Component(0,0,0,0, parent=mm)
        mm_exit_btn.resize_width_ratio(1/6)
        mm_exit_btn.resize_height_ratio(1/10)
        mm_exit_btn.center_x_percent(1/3)
        mm_exit_btn.center_y_percent(3/4)
        mm_exit_btn.set_font("calibri")
        mm_exit_btn.text = "Quit"
        mm_exit_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: self.close())

        mm_start_btn = Component(0,0,0,0, parent=mm)
        mm_start_btn.resize_width_ratio(1/6)
        mm_start_btn.resize_height_ratio(1/10)
        mm_start_btn.center_x_percent(2/3)
        mm_start_btn.center_y_percent(3/4)
        mm_start_btn.set_font("calibri")
        mm_start_btn.text = "Play"
        mm_start_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: print("Call code to go to next menu"))

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
                    exit(0)
            # Get the relative movement (velocity vector) of the mouse position per frame
            self.mouse_rel = pg.mouse.get_rel()            

            # Main Root update 
            self.current_component.update(self)
            self.current_component.render(self)

            pg.display.update()
            # Limit Game to 60 FPS
            clock.tick(60)

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
