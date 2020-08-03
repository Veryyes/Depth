import pygame as pg

from Component import Component
from Actions import Actions

'''
A Special type of component representing Dropdown menu (hence the name)
It interprets its children as the buttons in its menu
'''
# TODO float up to top level parent
class DropDownMenu(Component):
    def __init__(self, parent, click_toggles=False):
        Component.__init__(self, parent=parent)

        self.original_parent = parent
        # print(self.original_parent.children)
        if self.parent:
            self.parent.children.pop()
            top = self.parent
            while(top.parent):
                top = top.parent
        # print(top.__class__)
        # print(self.original_parent.children)
        self.parent = top
        self.parent.add_child(self)

        self.visible=False
        self.enabled=False

        self.highlight_factor = 1.25
        self.scroll_pos = 0

        self.padding = 8

        self.rect.w = self.original_parent.rect.w
        self.rect.h = self.original_parent.rect.h

        self.toggled = False

        if click_toggles:
            self.original_parent.register_event(Actions.on_click, self.show_menu, member_func=True)
            self.register_event(Actions.on_click_outside, self.hide_menu, member_func=True)
        else:
            self.original_parent.register_event(Actions.on_mouse_enter, self.show_menu, member_func=True)
            # TODO Override Actions.on_mouse_exit_family
            self.original_parent.register_event(Actions.on_mouse_exit_family, self.hide_menu, member_func=True)

        self.register_event(Actions.on_scroll_up, self.slide_buttons_up, member_func=True)
        self.register_event(Actions.on_scroll_down, self.slide_buttons_down, member_func=True)

    def slide_buttons_down(self, gctxt):
        scroll = int(self.rect.h / len(self.children)) * 3
        if self.children[-1].get_bottom_edge() > self.get_bottom_edge():
            for child in self.children:
                child.rect.y -= scroll
            self.update_button_visibility(gctxt)


    def slide_buttons_up(self, gctxt):
        scroll = int(self.rect.h / len(self.children)) * 3
        if self.children[0].rect.y <= self.rect.y:
            for child in self.children:
                child.rect.y += scroll
            self.update_button_visibility(gctxt)

    def calculate_max_height(self, gctxt):
        abs_max_heights = int(0.90 * (gctxt.screen_rect.h - self.rect.y))
        total_children_heights = sum([child.rect.h for child in self.children]) + self.padding * (len(self.children) - 1)

        return min(total_children_heights, abs_max_heights)

    def update_button_visibility(self, gctxt):
        max_height = self.calculate_max_height(gctxt)
        for child in self.children:
            too_low = child.rect.y + child.rect.h > self.rect.y + max_height
            too_high = child.rect.y < self.rect.y
            if too_low or too_high:
                child.visible=False
                child.enabled=False
            else:
                child.visible=True
                child.enabled=True

    '''
    Shows the dropdown menu and all its buttons
    :param gctxt: game context. Its here because the caller is the event action listener
    '''
    def show_menu(self, gctxt):
        if self.toggled:
            return

        self.toggled = True

        self.expanded = True

        self.visible=True
        self.enabled=True
    
        self.rect.y = self.original_parent.get_bottom_edge()
        self.resize_width_on_children()

        max_height = self.calculate_max_height(gctxt)

        self.update_button_visibility(gctxt)
        
        if len(self.children) > 0:
            self.rect.h = max_height


    '''
    Hides the dropdown menu and all its buttons
    :param gctxt: game context. Its here because the caller is the event action listener
    '''
    def hide_menu(self, gctxt):
        if self.toggled:
            return
            
        self.toggled = True

        self.expanded = False
        self.visible=False
        self.enabled=False
        self.disable_and_hide_children()
        self.rect.y = self.original_parent.rect.y
        self.rect.w = self.original_parent.rect.w
        self.rect.h = self.original_parent.rect.h
        

    '''
    Add a button (component) to the menu. Automatically adds the button as a child and repositions it
    :param button: The component to act as a button for this menu
    '''
    def add_button(self, button):
        self.add_child(button)
        button.text_align = (Component.LEFT, Component.CENTER)
        if(self.rect.w > button.rect.w):
            button.resize_width_ratio(1)
        button.highlight_on_hover(factor=self.highlight_factor)

        button_idx = self.children.index(button)
        if button_idx != 0:
            last = self.children[button_idx - 1]
            button.rect.y = last.get_bottom_edge() + self.padding
        else:
            button.rect.y = self.original_parent.get_bottom_edge() + self.padding

        

    def update(self, game_ctxt):
        super().update(game_ctxt)
        self.toggled = False

    # TODO modify
    def mouse_exited_family(self, game_ctxt):
        x, y = pg.mouse.get_pos()
        x_vel, y_vel = game_ctxt.mouse_rel

        prev_x = x-x_vel
        prev_y = y-y_vel

        family = [child for child in self.children]
        family.append(self)

        one_inside_before = any([member.rect.collidepoint(prev_x, prev_y)==1 for member in family])
        all_outside_after = all([not member.rect.collidepoint(x, y) for member in family])

        return one_inside_before and all_outside_after