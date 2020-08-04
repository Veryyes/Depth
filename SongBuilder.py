import pygame as pg

from Component import Component
from Actions import Actions

from DropdownMenu import DropDownMenu
from FilePicker import FilePicker

class SongBuilder(Component):
    def __init__(self, gctxt):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
        self.song = None
        self.gctxt = gctxt
        self.init_gui(gctxt)

    def init_gui(self, gctxt):        
        pass

    def exit_to_main_menu(self, gctxt):
        # TODO any clean up on component
        gctxt.change_to_main_menu()
