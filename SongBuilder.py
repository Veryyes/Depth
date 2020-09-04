import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

import librosa
import soundfile as sf
import numpy as np

from Project import Project

import IPython

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

        self.project = Project()
        wav, sr  = librosa.load(os.path.join('.', 'library', 'Niji no Kanata ni.wav'), sr=None)#'.\\library\\Niji no Kanata ni.wav', sr=None)
        self.wav_data = wav
        self.sample_rate = sr
        self.specto_data = None #TODO

        self.timeline_start = 0
        self.timeline_length = 60

        self.init_menu_bar()
        self.init_gui()

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

        save_act = QAction("Save", self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip("Save Project")
        save_act.triggered.connect(self.save_project)

        save_as_act = QAction("Save as", self)
        save_as_act.setShortcut("Ctrl+Shift+S")
        save_as_act.setStatusTip("Save Project As")
        save_as_act.triggered.connect(self.save_as_project)

        export_act = QAction("Export", self)
        export_act.setShortcut("Ctrl+E")
        export_act.setStatusTip("Export to a Song File")
        export_act.triggered.connect(self.export)

        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addMenu(self.recent_expand)
        file_menu.addAction(close_act)
        file_menu.addAction(save_act)
        file_menu.addAction(save_as_act)
        file_menu.addAction(export_act)

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
        credit_act.triggered.connect(self.show_credits)
        help_menu.addAction(credit_act)

    def show_credits(self):
        QMessageBox.about(self, 'Credits', 'By Yours Truly, Veryyes')

    def init_gui(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(64,61,84))
        self.setPalette(p)

        grid = QGridLayout()
        
        # Row 0 - things
        m = MetadataView(self.project, self)
        grid.addWidget(m, 0, 0)

        l = LyricsView(self.project, self)
        grid.addWidget(l, 0, 1)

        # Row 1 - db/time graph
        av = AudioView(self.wav_data, self.sample_rate, parent=self)
        grid.addWidget(av, 1, 0, 1, 4)

        # Row 2 - timeline
        timeline = Timeline()
        grid.addWidget(timeline, 2, 0, 1, 4)

        # Relative Row Heights
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 2)


        main_widget = QWidget()
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)

    def load_audiofile(self, filepath):
        if not os.path.exists(filepath):
            QMessageBox.warning(self, "File does not exist", "{} Does not exists".format(filepath))
            return
        self.project.audio_path = filepath
        wav, sr  = librosa.load(filepath, sr=None)
        self.sound_data = wav
        self.sample_rate = sr
        self.project.song_length = 1000 * (sr/wav.shape[0])
        self.project.sample_rate = self.sample_rate

    def new_project(self):
        # Open file dialog to pick a song
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getOpenFileName(self, "Import a Song", "","All Files (*)", options=options)
        if filepath:
            self.project = Project()
            self.load_audiofile(filepath)


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
        
        # Now we actually try to load the project in
        try:
            self.project = Project.from_json(filename)
        except Exception as e:
            err_msg = QMessageBox()
            err_msg.setWindowTitle("Unable to Load Project")
            err_msg.setText("Invalid File Format")
            err_msg.exec_()
            return

        #TODO enable components

    def close_project(self):
        # TODO if has modified since last save, prompt user for save
        self.project = None
        # TODO disable components

    def save_project(self):
        if self.project is not None:
            if self.project.filepath is not None:
                self.project.to_json()
            else:
                self.save_as_project()

    def save_as_project(self):
        pass

    def enable_components(self):
        pass

    def disable_components(self):
        pass

    def export(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass
        

class Timeline(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,300,192)
        self.show()

class LyricsView(QWidget):
    def __init__(self, project, parent=None):
        QWidget.__init__(self, parent)
        self.project = project
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.lyrics_box = QTextEdit(self)
        self.lyrics_box.textChanged.connect(self.text_update)
        layout.addWidget(self.lyrics_box)
        self.setLayout(layout)

    def text_update(self):
        print(self.lyrics_box.toPlainText())

class MetadataView(QWidget):
    def __init__(self, project, parent=None):
        QWidget.__init__(self, parent)
        self.project = project
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        audio_lbl = QLabel(self)
        audio_lbl.setText("Audio: {}".format(os.path.basename(str(self.project.audio_path))))

        song_duration_lbl = QLabel(self)
        song_duration_lbl.setText("Duration {}:{}".format(int(self.project.song_length/60), self.project.song_length%60))

        sample_rate_lbl = QLabel(self)
        sample_rate_lbl.setText("Sample Rate: {} Hz".format(self.project.sample_rate))

        layout.addWidget(audio_lbl)
        layout.addWidget(song_duration_lbl)
        layout.addWidget(sample_rate_lbl)

        self.setLayout(layout)

class AudioView(QWidget):
    def __init__(self, audio_data, sample_rate, parent=None):       
        QWidget.__init__(self, parent)
        self.parent = parent
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.song_duration = self.audio_data.shape[0]/self.sample_rate
        self.max_amplitude = max(self.audio_data) * 1.1

        # Interval between graphed samples (Because graphing all of them takes a long time)
        self.interval = .001 
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(46, 70, 125))
        self.setPalette(p)

    def get_timeline_start(self):
        return self.parent.timeline_start

    def get_timeline_length(self):
        return self.parent.timeline_length

    def plot_wav(self):
        plot_width = self.geometry().width()
        plot_height = self.geometry().height()
        center = int(plot_height / 2.0)

        time_range = np.arange(self.get_timeline_start(), self.get_timeline_start() + self.get_timeline_length(), self.interval)
        samples = librosa.time_to_samples(time_range, sr=self.sample_rate)

        self.max_amplitude = 2*max(self.audio_data[samples[0] : samples[-1]])

        index = 0
        for sample in samples:
            x = (float(index)/samples.size) * plot_width
            y = (self.audio_data[sample]/self.max_amplitude) * plot_height + center
            index += 1

            yield x, y

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        qp.setPen(QColor(58, 181, 87))
        self.waveform = [point for point in self.plot_wav()]
        for i in range(len(self.waveform) - 1):
            point1 = self.waveform[i]
            point2 = self.waveform[i+1]
            qp.drawLine(point1[0], point1[1], point2[0], point2[1])
        qp.end()        


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

# f = '.\\library\\Niji no Kanata ni.mp3'
# import os
# print(os.path.exists(f))
# song = AudioSegment.from_mp3(f)
# play(song)
