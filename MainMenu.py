import pygame as pg

from Component import Component
from Actions import Actions

class MainMenu(Component):
    def __init__(self, gctxt):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
        self.image = gctxt.resources.get_image("mm_back.png")
        self.set_font('broadway')
        self.text = ("Depth")

        self.exit_btn = Component(0,0,0,0, parent=self)
        self.exit_btn.resize_width_ratio(1/6)
        self.exit_btn.resize_height_ratio(1/10)
        self.exit_btn.center_x_percent(1/3)
        self.exit_btn.center_y_percent(3/4)
        self.exit_btn.set_font("calibri")
        self.exit_btn.text = "Quit"
        self.exit_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: gctxt.close())

        self.start_btn = Component(0,0,0,0, parent=self)
        self.start_btn.resize_width_ratio(1/6)
        self.start_btn.resize_height_ratio(1/10)
        self.start_btn.center_x_percent(2/3)
        self.start_btn.center_y_percent(3/4)
        self.start_btn.set_font("calibri")
        self.start_btn.text = "Play"
        self.start_btn.register_event(Actions.on_left_click, 
                                    lambda c, gctxt: print("Call code to go to next menu"))