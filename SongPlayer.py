import queue

import pygame as pg

from Component import Component
from Actions import Actions
import ResourceManager

class SongPlayer(Component):
    def __init__(self, gctxt, current_song=None):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
        
        self.song_queue = queue.Queue() # Thread Safe Queue
        # Cant peek a queue.Queue(), so just store the current and next here
        self.current_song = current_song
        self.next_song = None

        # Default Black Background
        self.image = pg.Surface((self.rect.w, self.rect.h))
        self.image.fill(0x0)

        # Time left on song
        self.time_left = Component(0,0,0,0, parent=self)
        self.time_left.set_font('verdana')
        self.time_left.text_color = (255,255,255)
        self.time_left.set_text("00:00")
        self.time_left.resize_width_ratio(1/3)
        self.time_left.resize_height_ratio(1/20)
        self.time_left.center_x_ratio(1/2)
        self.time_left.flush_top()
        self.time_left.rect.y += 16

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

        # Settings 
        self.settings_btn = Component(0,0,0,0, parent=self)
        self.settings_btn.set_font("calibri", size=self.font_size/3)
        self.settings_btn.text_color = (255,255,255)
        self.settings_btn.set_text("Settings", allow_resize=True)
        self.settings_btn.flush_bottom()
        self.settings_btn.rect.y -= 16
        self.settings_btn.flush_right()
        self.settings_btn.rect.x -= 16
        self.settings_btn.register_event(Actions.on_left_click, self.open_settings, member_func=True)


        # Current Song
        self.current_lbl = Component(0,0,0,0, parent=self)
        self.current_lbl.set_font("calibri", size=self.font_size/2)
        self.current_lbl.text_color = (255,255,255)
        self.current_lbl.set_text(self.current_song, allow_resize=True)
        self.current_lbl.flush_top()
        self.current_lbl.rect.y += 16
        self.current_lbl.flush_left()
        self.current_lbl.rect.x += 16
        self.current_lbl.register_event(Actions.on_left_click, self.play, member_func=True)

        # Next Song
        self.next_lbl = Component(0,0,0,0, parent=self)
        self.next_lbl.set_font("calibri", size=self.font_size/2)
        self.next_lbl.text_color = (255,255,255)
        self.next_lbl.set_text(self.next_song, allow_resize=True)
        self.next_lbl.flush_top()
        self.next_lbl.rect.y += 16
        self.next_lbl.flush_right()
        self.next_lbl.rect.x -= 16

    def exit_to_main_menu(self, gctxt):
        # TODO clear current song
        gctxt.change_to_main_menu()

    def open_settings(self, gctxt):
        # TODO Implement
        print("Open settings...")

    def play(self, gctxt):
        #sound = ResourceManager.get_audio(self.current_song)
        print('playing {}'.format(self.current_song))
        pg.mixer.music.load(ResourceManager.get_music_path(self.current_song))
        pg.mixer.music.play(0)