import queue
import json

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

        self.playing = False
        self.paused = False
        self.pause_time = 0
        self.total_pause_time = 0
        self.start = 0
        self.song_time = 0
        self.lyric_counter = 0
        with open("library\\Niji no Kanata ni.lyc", 'r') as f:
            self.song = json.load(f)

        self.pre_fade_ratio = .75

        self.init_gui(gctxt)

    def init_gui(self, gctxt):
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

        self.lyrics_1 = Component(0,0,0,0, parent=self)
        self.lyrics_1.set_font("calibri")
        self.lyrics_1.text_color = (255, 255, 255)
        self.lyrics_1.set_text("", allow_resize=True)
        self.lyrics_1.center_y_ratio(3/4)
        self.lyrics_1.center_x_ratio(1/2)

        self.lyrics_2 = Component(0,0,0,0, parent=self)
        self.lyrics_2.set_font("calibri")
        self.lyrics_2.text_color = (255, 255, 255)
        self.lyrics_2.set_text("", allow_resize=True)
        self.lyrics_2.center_y_ratio(5/6)
        self.lyrics_2.center_x_ratio(1/2)

        self.subtitles = [self.lyrics_1, self.lyrics_2]

    def exit_to_main_menu(self, gctxt):
        if not self.paused:
            self.toggle_pause(gctxt)
        
        gctxt.change_to_main_menu()

    def open_settings(self, gctxt):
        # TODO Implement
        if not self.paused:
            self.toggle_pause(gctxt)
        print("Open settings...")

    def play(self, gctxt):
        if self.paused:
            return self.toggle_pause(gctxt)

        print('playing {}'.format(self.current_song))
        pg.mixer.music.load(ResourceManager.get_music_path(self.current_song))
        self.playing = True
        self.start = pg.time.get_ticks()
        pg.mixer.music.play(0)

    def stop(self, gctxt):
        pg.mixer.music.stop()
        pg.mixer.music.unload()
        self.playing = False

    def skip(self, gctxt):
        self.stop(gctxt)
        self.current_song = self.next_song
        self.next_song = self.song_queue.get()
        self.play(gctxt)

    def toggle_pause(self, gctxt):
        if self.paused:
            self.playing = True
            self.total_pause_time += (pg.time.get_ticks() - self.pause_time)
            self.pause_time = 0
            pg.mixer.music.unpause()
        else:
            self.playing = False
            self.pause_time = pg.time.get_ticks()
            pg.mixer.music.pause()

    def _calcuate_alpha_on_delta(self, start_time, end_time, curve='linear'):
        if curve == 'linear':
            diff = end_time - start_time
            progress = self.song_time - start_time
            return int(255 * (progress / diff))

    def update(self, game_ctxt):
        super().update(game_ctxt)

        if not self.playing:
            return

        self.song_time = pg.time.get_ticks() - self.start
        self.time_left.set_text(str(self.song_time))
        self.time_left.center_x_ratio(1/2)

        self._update_lyrics(game_ctxt)

        # TODO if song ends...
        

    def _update_lyrics(self, game_ctxt):
        mappings = self.song['mapping']

        if self.lyric_counter >= len(mappings):
            return

        curr_map = mappings[self.lyric_counter]
        prev_map = mappings[self.lyric_counter - 1 if self.lyric_counter > 0 else 0]
        if self.lyric_counter + 1 < len(mappings):
            next_map = mappings[self.lyric_counter + 1]
        else:
            next_map = None

        #.----------------------------------------------------.
        #|   |     L1      |   |    L2      |                 | 
        #`----------------------------------------------------'
        #    t1            t2  t3           t4
        # assuptions: t1 < t3 && t2 < t4 
        #    i.e. L2 !contained L1 or vice versa

        if self.lyric_counter == 0:
            if self.song_time > (curr_map['start'] - 3000) and self.song_time < curr_map['start']:
                alpha = self._calcuate_alpha_on_delta(curr_map['start'] - 3000, curr_map['start'])
                self.subtitles[0].set_text(curr_map['lyrics'], allow_resize=True, color=(255, 255, 255, alpha))
                self.subtitles[0].center_x_ratio(1/2)


        current_label = self.subtitles[(self.lyric_counter)%2]
        next_label = self.subtitles[(self.lyric_counter+1)%2]

        curr_map_duration = curr_map['end'] - curr_map['start']
        pre_fade = int(self.pre_fade_ratio * curr_map_duration)

        # t3 - b < t < t3
        if next_map is not None and next_map['start'] - pre_fade < self.song_time and self.song_time < next_map['start']:
            #Start Loading in Lyrics 2
            alpha = self._calcuate_alpha_on_delta((curr_map['end'] - pre_fade), curr_map['end'])
            if alpha > 255:
                alpha = 255
            next_label.set_text(mappings[self.lyric_counter + 1]['lyrics'], allow_resize=True, color=(255,255,255, alpha))
            next_label.center_x_ratio(1/2)

        # t2 < t
        if self.song_time > curr_map['end']:
            current_label.set_text_color((255,255,255, 0))
        
        if next_map is not None and self.song_time > next_map['start']:
            self.lyric_counter += 1

