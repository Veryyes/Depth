import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from Project import Project

class SongBuilder(QMainWindow):
    INSTALL_FOLDER = os.getcwd()
    CFG_PATH = os.path.join(INSTALL_FOLDER, "configs.json")
    HIST_PATH = os.path.join(INSTALL_FOLDER, "hist.json")
    CFG=dict()
    HIST={'recent_files':[]}

    def __init__(self, *args, **kwargs):
        super(SongBuilder, self).__init__(*args, **kwargs)
        self.setWindowTitle("Depth Song Builder")
        self.resize(1280,720)
        self.center_screen()        
        self.load_persistant_data()
        self.statusBar().showMessage('Ready')
        self.init_menu_bar()

        self.current_project = None

        grid = QGridLayout()
        
        # grid.addWidget(QLabel("dicks"), 0, 0)
        # grid.addWidget(QLabel("dicks"), 1, 0)
        # grid.addWidget(QLabel("dicks"), 1, 1)
        # grid.addWidget(QLabel("dicks"), 2, 1)


        main_widget = QWidget()
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)

    def load_persistant_data(self):
        if not os.path.exists(self.CFG_PATH):
            with open(self.CFG_PATH, 'w') as f:
                json.dump(self.CFG, f)
        if not os.path.exists(self.HIST_PATH):
            with open(self.HIST_PATH, 'w') as f:
                json.dump(self.HIST, f)

        with open(self.CFG_PATH, 'r') as f:
            self.CFG = json.load(f)
        with open(self.HIST_PATH, 'r') as f:
            self.HIST = json.load(f)

    def save_persistant_data(self):
        print("Saving")
        with open(self.CFG_PATH, 'w') as f:
            json.dump(self.CFG, f)
        with open(self.HIST_PATH, 'w') as f:
            json.dump(self.HIST, f)

    def center_screen(self):
        center_pt = QDesktopWidget().availableGeometry().center()
        rect = self.frameGeometry()
        rect.moveCenter(center_pt)
        self.move(rect.topLeft())
    
    def init_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        new_act = QAction("New", self)
        new_act.setShortcut('Ctrl+N')
        new_act.setStatusTip("New Lyrics Project")
        new_act.triggered.connect(self.new_project)

        open_act = QAction("Open", self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip("Open Lyrics Project")
        open_act.triggered.connect(self.open_project)

        self.recent_expand = QMenu('Recent Files', self)
        for recent in self.HIST['recent_files']:
            recent_act = QAction(recent, self)
            recent_act.triggered.connect(lambda: self.load_project(recent))
            self.recent_expand.addAction(recent_act)

        close_act = QAction("Close", self)
        close_act.setShortcut('Ctrl+W')
        close_act.setStatusTip("Close Project")
        close_act.triggered.connect(self.close_project)

        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addMenu(self.recent_expand)
        file_menu.addAction(close_act)

        edit_menu = menubar.addMenu("&Edit")
        undo_act = QAction("&Undo", self)
        undo_act.setShortcut('Ctrl+Z')
        undo_act.triggered.connect(self.undo)

        redo_act = QAction("&Redo", self)
        redo_act.setShortcut("Ctrl+Y")
        redo_act.triggered.connect(self.redo)

        edit_menu.addAction(undo_act)
        edit_menu.addAction(redo_act)
        
        help_menu = menubar.addMenu("&Help")
        credit_act = QAction("Credits", self)
        credit_act.triggered.connect(lambda: print("Made by Yours Truly, Veryyes"))

    def new_project(self):
        self.current_project = Project()

    def open_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open a Project", "","All Files (*);;Lyric Files (*.lyc)", options=options)
        if filename:
            self.load_project(filename)

    def load_project(self, filename):
        # If already in the recent list, remove it; we add it at the top of the list below
        try:
            idx = self.HIST['recent_files'].index(filename)
            del self.HIST['recent_files'][idx]
            self.recent_expand.removeAction(self.recent_expand.actions()[idx])
        except ValueError:
            # I wish python had a nicer way to get the index of something without throwing an exception...
            pass
            
        # Register File to recently opened
        self.HIST['recent_files'].insert(0, filename)
        recent_act = QAction(filename, self)
        recent_act.triggered.connect(lambda: self.load_project(filename))
        if len(self.recent_expand.actions()) > 0:
            self.recent_expand.insertAction(self.recent_expand.actions()[0], recent_act)
        else:
            self.recent_expand.addAction(recent_act)
        # If we have more than 10, drop the oldest
        if len(self.HIST['recent_files']) > 10:
            self.HIST['recent_files'].pop()
            self.recent_expand.removeAction(self.recent_expand.actions()[-1])
        

        self.current_project = Project.load(filename)

        #TODO enable components

    def close_project(self):
        if self.current_project is not None:
            self.current_project.save()
            self.current_project = None
        # TODO disable components

    def enable_components(self):
        pass

    def disable_components(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass
        
        

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    sb = SongBuilder()
    sb.show()
    exit_num = 1
    try:
        exit_num = app.exec_()
    except KeyboardInterrupt:
        pass
    finally:
        # Always save our configs pls
        sb.save_persistant_data()
        sys.exit(exit_num)