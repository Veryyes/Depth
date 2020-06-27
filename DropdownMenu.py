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

    '''
    Add a button (component) to the menu. Automatically adds the button as a child and repositions it
    :param button: The component to act as a button for this menu
    :param padding: (Optional) The padding between this button and the one previous or from the top of menu if its the first button
    '''
    def add_button(self, button, padding=8):
        self.add_child(button)

        button_idx = self.children.index(button)
        if button_idx != 0:
            last = self.children[button_idx - 1]
            button.rect.y = last.get_bottom_edge() + padding
        else:
            button.rect.y += padding

        self.resize_width_on_children()
        self.rect.h = max([child.rect.y+child.rect.h for child in self.children]) - self.rect.y 
