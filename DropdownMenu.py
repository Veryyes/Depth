import pygame as pg

from Component import Component
from Actions import Actions

'''
A Special type of component representing Dropdown menu (hence the name)
It interprets its children as the buttons in its menu
'''
class DropDownMenu(Component):
    def __init__(self, parent):
        Component.__init__(self, parent=parent)
        self.visible=False
        self.enabled=False

        self.rect.w = self.parent.rect.w
        self.rect.h = self.parent.rect.h

        self.parent.register_event(Actions.on_mouse_enter, self.show_menu, member_func=True)
        self.parent.register_event(Actions.on_mouse_exit_family, self.hide_menu, member_func=True)

    '''
    Shows the dropdown menu and all its buttons
    :param gctxt: game context. Its here because the caller is the event action listener
    '''
    def show_menu(self, gctxt):
        self.visible=True
        self.enabled=True
        self.enable_and_show_children()

        self.rect.y = self.parent.get_bottom_edge()
        self.resize_width_on_children()
        self.rect.h = max([child.rect.y+child.rect.h for child in self.children]) - self.rect.y 

    '''
    Hides the dropdown menu and all its buttons
    :param gctxt: game context. Its here because the caller is the event action listener
    '''
    def hide_menu(self, gctxt):
        self.visible=False
        self.enabled=False
        self.disable_and_hide_children()
        self.rect.y = self.parent.rect.y
        self.rect.w = self.parent.rect.w
        self.rect.h = self.parent.rect.h
        

    '''
    Add a button (component) to the menu. Automatically adds the button as a child and repositions it
    :param button: The component to act as a button for this menu
    :param padding: (Optional) The padding between this button and the one previous or from the top of menu if its the first button
    '''
    def add_button(self, button, padding=8):
        self.add_child(button)

        button.register_event(
            Actions.on_mouse_enter,
            # Takes each color component and multiples it by 1.25 of the parents background color
            lambda c, gctxt: c.set_background_color(tuple(map(lambda color: int(color*1.25) , c.parent.background_color)))
        )

        button.register_event(
            Actions.on_mouse_exit,
            lambda c, gctxt: c.set_background_color(c.parent.background_color)
        )

        button_idx = self.children.index(button)
        if button_idx != 0:
            last = self.children[button_idx - 1]
            button.rect.y = last.get_bottom_edge() + padding
        else:
            button.rect.y = self.parent.get_bottom_edge() + padding
