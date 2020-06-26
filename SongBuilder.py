import pygame as pg

from Component import Component
from Actions import Actions

class SongBuilder(Component):
    def __init__(self, gctxt):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
    
        # Default Grey Background
        self.image = pg.Surface((self.rect.w, self.rect.h))
        self.image.fill((32,32,32)) 

        # Exit to main menu
        self.exit_btn = Component(0,0,0,0, parent=self)
        self.exit_btn.set_font("calibri", size=self.font_size/3)
        self.exit_btn.text_color = (255,255,255)
        self.exit_btn.set_text("Exit to Main Menu", allow_resize=True)
        self.exit_btn.flush_bottom()
        self.exit_btn.rect.y -= 16
        self.exit_btn.flush_left()
        self.exit_btn.rect.x += 16
        self.exit_btn.register_event(Actions.on_left_click, self.exit_to_main_menu, member_func=True)

    def exit_to_main_menu(self, gctxt):
        # TODO any clean up on component
        gctxt.change_to_main_menu()