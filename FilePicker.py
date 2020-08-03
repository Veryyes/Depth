import os
from sys import platform
import re

import pygame as pg
import psutil

from Component import Component
from Actions import Actions
import ResourceManager

from DropdownMenu import DropDownMenu

class FilePicker(Component):
    def __init__(self, gctxt, parent=None, default_path=None):
        Component.__init__(self, parent=parent)
        self.gctxt = gctxt
        self.os = None
        # Assuming the user's home directory exists...    
        if platform.startswith('linux'):
            self.os = 'linux'
            self.home_dir = os.path.expandvars('$HOME')
        elif platform.startswith('win32') or platform.startswith('cygwin'):
            self.os = 'windows'
            self.home_dir = os.path.expandvars('%userprofile%')
        elif platform.startswith('darwin'):
            self.os = 'mac'
            #I dont own a mac, no clue what home dir is? same as linux??
        
        if not default_path:
            self.path = os.path.join(self.home_dir, 'Documents')
        else:
            self.path = default_path

        if not os.path.exists(self.path):
            self.path = self.home_dir

        self.win_drive_pattern = re.compile(r'^[A-Z]:\\$')

        # self.visible=False
        # self.enabled=False

        self.set_background_color((96,96,96))
        self.draw_outline=True
        self.outline_thiccness = 1
        self.resize_width_ratio(3/4, component=gctxt.current_component)
        self.resize_height_ratio(3/4, component=gctxt.current_component)
        self.center_x_ratio(1/2, component=gctxt.current_component)
        self.center_y_ratio(.45, component=gctxt.current_component)
        
        font_scale = self.parent.get_diagonal()/50

        #title bar
        title_bar = Component(parent=self)
        title_bar.set_background_color((128,128,128))
        title_bar.set_font("verdana", size = font_scale)
        title_bar.set_text("Select a File", allow_resize=True)
        title_bar.resize_width_ratio(1)
        title_bar.draw_outline=True
        title_bar.outline_thiccness = 1
        #TODO add drag feature? :O

        close_btn = Component(parent=title_bar)
        close_btn.set_text("×", allow_resize=True)
        close_btn.flush_right()
        close_btn.highlight_on_hover()
        close_btn.register_event(Actions.on_left_click, self.close, member_func=True)

        # Main body
        container = Component(parent=self)
        container.resize_width_ratio(1)
        container.rect.y = title_bar.get_bottom_edge()
        container.rect.h = self.rect.h - title_bar.rect.h
        container.set_font("calibri", size = font_scale*.8)

        address_bar = Component(parent=container)
        address_bar.resize_width_ratio(3/4)
        address_bar.rect.y += 4
        address_bar.center_x_ratio(1/2)

        look_in_lbl = Component(parent=address_bar)
        look_in_lbl.set_text("Look in:", allow_resize=True)
        look_in_lbl.left_align_ratio(1/10)
        
        self.curr_dir_bar = Component(parent=address_bar)
        self.curr_dir_bar.background = True
        self.curr_dir_bar.set_background_color((255,255,255))
        self.curr_dir_bar.resize_width_ratio(3/6)
        self.curr_dir_bar.rect.h = look_in_lbl.rect.h
        self.curr_dir_bar.rect.x = look_in_lbl.get_right_edge() + 8
        self.curr_dir_bar.set_text(os.path.basename(self.path))
        self.curr_dir_bar.text_align = (Component.LEFT, Component.CENTER)

        address_bar.resize_height_on_children()

        arrow_down = Component(parent=self.curr_dir_bar)
        arrow_down.image = ResourceManager.get_image("arrow_dn.png")
        arrow_down.fit_image((self.curr_dir_bar.rect.h, self.curr_dir_bar.rect.h))
        arrow_down.flush_right()

        self.curr_dir_dropdown = DropDownMenu(self.curr_dir_bar, click_toggles=True)
        self.curr_dir_dropdown.background=True
        self.curr_dir_dropdown.set_background_color((192,192,192))
        self.curr_dir_dropdown.highlight_factor = 0.5

        directories = self.get_user_home_dirs() + self.get_root_dirs() + self.get_desktop_dirs()
        for directory in directories:
            button = Component(parent=self.curr_dir_dropdown)
            if self.win_drive_pattern.match(directory):
                button.set_text(directory, allow_resize=True)
            else:
                button.set_text(os.path.basename(directory), allow_resize=True)

            button.full_path = directory
            button.background=True
            self.curr_dir_dropdown.add_button(button)
            # Im sorry
            button.register_event(Actions.on_click, lambda c, gctxt: c.parent.original_parent.parent.parent.parent.set_path(c.full_path))

        quick_access = Component(parent=container)
        quick_access.flush_left()
        quick_access.rect.y = address_bar.get_bottom_edge()
        quick_access.resize_width_ratio(1/6)
        quick_access.resize_height_ratio(4/5)

        desktop_btn = Component(parent=quick_access)
        desktop_btn.flush_left()
        desktop_btn.rect.x += 8
        desktop_btn.flush_top()
        desktop_btn.resize_width_ratio(1)
        desktop_btn.resize_height_ratio(1/3)
        desktop_btn.image = ResourceManager.get_image('desktop.png')
        desktop_btn.fit_image()
        desktop_btn.set_text("Desktop")
        desktop_btn.text_align = (Component.CENTER, Component.BOTTOM)
        desktop_btn.highlight_on_hover()
        desktop_btn.path = os.path.join(self.home_dir, "Desktop")
        desktop_btn.register_event(Actions.on_click, lambda c, gctxt: c.parent.parent.parent.set_path(c.path))

        libraries_btn = Component(parent=quick_access)
        libraries_btn.flush_left()
        libraries_btn.rect.x += 8
        libraries_btn.rect.y = desktop_btn.get_bottom_edge()
        libraries_btn.resize_width_ratio(1)
        libraries_btn.resize_height_ratio(1/3)
        libraries_btn.image = ResourceManager.get_image('library.png')
        libraries_btn.fit_image()
        libraries_btn.set_text("Libraries")
        libraries_btn.text_align = (Component.CENTER, Component.BOTTOM)
        libraries_btn.highlight_on_hover()
        libraries_btn.path = self.home_dir
        libraries_btn.register_event(Actions.on_click, lambda c, gctxt: c.parent.parent.parent.set_path(c.path))

        thispc_btn = Component(parent=quick_access)
        thispc_btn.flush_left()
        thispc_btn.rect.x += 8
        thispc_btn.rect.y = libraries_btn.get_bottom_edge()
        thispc_btn.resize_width_ratio(1)
        thispc_btn.resize_height_ratio(1/3)
        thispc_btn.image = ResourceManager.get_image('this_pc.png')
        thispc_btn.fit_image()
        thispc_btn.set_text("This PC")
        thispc_btn.text_align = (Component.CENTER, Component.BOTTOM)
        thispc_btn.highlight_on_hover()
        thispc_btn.register_event(Actions.on_click, lambda c, gctxt: c.parent.parent.parent.set_path('/'))
        
        file_view = Component(parent=container)
        file_view.resize_width_ratio(5/6)
        file_view.rect.w -= 8
        file_view.resize_height_ratio(4/5)
        file_view.flush_right()
        file_view.rect.y = address_bar.get_bottom_edge()
        file_view.background = True
        file_view.set_background_color = ((255,255,255))

        
    def set_path(self, path):
        if self.os == 'windows' and path == '/':
            self.path = 'This PC'
        else:
            self.path = path
        self.curr_dir_bar.set_text(os.path.basename(self.path))
        self.curr_dir_dropdown.hide_menu(self.gctxt)

    def get_user_home_dirs(self):
        dirs = list()

        for filepath in os.listdir(self.home_dir):
            full_path = os.path.join(self.home_dir, filepath)
            if os.path.isdir(full_path):
                dirs.append(filepath)

        return dirs

    def get_desktop_dirs(self):
        desktop_dir = os.path.join(self.home_dir, "Desktop")
        dirs = list()

        if os.path.exists(desktop_dir):
            for filepath in os.listdir(desktop_dir):
                full_path = os.path.join(desktop_dir, filepath)
                if os.path.isdir(full_path):
                    dirs.append(filepath)

        return dirs

    def get_root_dirs(self):
        partitions = psutil.disk_partitions()
        return [p.mountpoint for p in partitions]
      
    def close(self, gctxt):
        self.visible=False
        self.enabled=False