import pygame as pg

from Component import Component
from Actions import Actions
import ResourceManager

class MainMenu(Component):
    def __init__(self, gctxt):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
        self.image = ResourceManager.get_image("mm_back.png")
        self.strech_image()
        self.set_font('broadway')
        self.set_text("Depth")

        self.exit_btn = Component(parent=self)
        self.exit_btn.resize_width_ratio(1/6)
        self.exit_btn.resize_height_ratio(1/10)
        self.exit_btn.center_x_ratio(1/4)
        self.exit_btn.center_y_ratio(3/4)
        self.exit_btn.set_font("calibri")
        self.exit_btn.set_text("Quit")
        self.exit_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: gctxt.close())

        self.start_btn = Component(parent=self)
        self.start_btn.resize_width_ratio(1/6)
        self.start_btn.resize_height_ratio(1/10)
        self.start_btn.center_x_ratio(1/2)
        self.start_btn.center_y_ratio(3/4)
        self.start_btn.set_font("calibri")
        self.start_btn.set_text("Play")
        self.start_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: gctxt.change_to_song_player())

        self.build_btn = Component(parent=self)
        self.build_btn.resize_width_ratio(1/6)
        self.build_btn.resize_height_ratio(1/10)
        self.build_btn.center_x_ratio(3/4)
        self.build_btn.center_y_ratio(3/4)
        self.build_btn.set_font("calibri")
        self.build_btn.set_text("Build")
        self.build_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: gctxt.launch_song_builder())