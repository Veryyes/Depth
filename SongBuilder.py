import pygame as pg

from Component import Component
from DropdownMenu import DropDownMenu
from Actions import Actions

class SongBuilder(Component):
    def __init__(self, gctxt):
        Component.__init__(self, gctxt.screen_rect.x, gctxt.screen_rect.y, gctxt.screen_rect.w, gctxt.screen_rect.h)
        self.song = None

        self.set_background_color((32,32,32))

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

        self.tool_bar = Component(parent=self)
        self.tool_bar.flush_top()
        self.tool_bar.resize_width_ratio(1)
        self.tool_bar.resize_height_ratio(1/24)
        self.tool_bar.set_background_color((86, 86, 86))
        
        padding = 16
        font_scale = gctxt.screen_diagonal()/50

        ###### FILE MENU ######
        self.file_btn = Component(parent=self.tool_bar)
        self.file_btn.flush_top()
        self.file_btn.rect.y += 2
        self.file_btn.flush_left()
        self.file_btn.rect.x += 2
        self.file_btn.set_font("calibri", size=font_scale)
        self.file_btn.set_text("File", allow_resize=True)

        file_menu = DropDownMenu(self.file_btn)
        file_menu.set_background_color((128,128,128))
        
        #new, open, recent, close
        new_btn = Component(parent=file_menu)
        new_btn.set_text("New", allow_resize=True)
        new_btn.background=True
        file_menu.add_button(new_btn)
        
        open_btn = Component(parent=file_menu)
        open_btn.set_text("Open", allow_resize=True)
        open_btn.background=True
        file_menu.add_button(open_btn)

        recent_btn = Component(parent=file_menu)
        recent_btn.set_text("Recent", allow_resize=True)
        recent_btn.background=True
        file_menu.add_button(recent_btn)

        close_btn = Component(parent=file_menu)
        close_btn.set_text("Close", allow_resize=True)
        close_btn.background=True
        file_menu.add_button(close_btn)

        ###### EDIT MENU ######
        self.edit_btn = Component(parent=self.tool_bar)
        self.edit_btn.flush_top()
        self.edit_btn.rect.y += 2
        self.edit_btn.rect.x = self.file_btn.get_right_edge() + padding
        self.edit_btn.set_font("calibri", size=font_scale)
        self.edit_btn.set_text("Edit", allow_resize=True)

        edit_menu = DropDownMenu(self.edit_btn)
        edit_menu.set_background_color((128,128,128))

        # Undo, Redo, Cut, Delete, Copy, Paste
        undo_btn = Component(parent=edit_menu)   
        undo_btn.set_text("Undo", allow_resize=True)
        undo_btn.background = True
        edit_menu.add_button(undo_btn)

        redo_btn = Component(parent=edit_menu)
        redo_btn.set_text("Redo", allow_resize=True)
        redo_btn.background = True
        edit_menu.add_button(redo_btn)

        cut_btn = Component(parent=edit_menu)
        cut_btn.set_text("Cut", allow_resize=True)
        cut_btn.background = True
        edit_menu.add_button(cut_btn)

        delete_btn = Component(parent=edit_menu)
        delete_btn.set_text("Delete", allow_resize=True)
        delete_btn.background = True
        edit_menu.add_button(delete_btn)

        copy_btn = Component(parent=edit_menu)
        copy_btn.set_text("Copy", allow_resize=True)
        copy_btn.background = True
        edit_menu.add_button(copy_btn)

        paste_btn = Component(parent=edit_menu)
        paste_btn.set_text("Paste", allow_resize=True)
        paste_btn.background = True
        edit_menu.add_button(paste_btn)


        self.help_btn = Component(parent=self.tool_bar)
        self.help_btn.flush_top()
        self.help_btn.rect.y += 2
        self.help_btn.rect.x = self.edit_btn.get_right_edge() + padding
        self.help_btn.set_font("calibri", size=font_scale)
        self.help_btn.set_text("Help", allow_resize=True)
        
        self.tool_bar.apply_to_children(False, 
            lambda child, kwargs: child.register_event(Actions.on_mouse_enter, lambda c, gctxt: c.set_background_color((64,64,64,255))))

        self.tool_bar.apply_to_children(False, 
            lambda child, kwargs: child.register_event(Actions.on_mouse_exit, lambda c, gctxt: c.set_background_color(c.parent.background_color)))


    def exit_to_main_menu(self, gctxt):
        # TODO any clean up on component
        gctxt.change_to_main_menu()
