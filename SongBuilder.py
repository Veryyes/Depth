import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

import librosa
import soundfile as sf
import numpy as np

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

        self.filename = None
        self.project = None
        wav, sr  = librosa.load('.\\library\\Niji no Kanata ni.wav', sr=None)
        # self.waveform_view = AudioView(wav, parent=self)
        # self.spectogram_view = AudioView(np.zeros([1,2], dtype=float))
        self.wav_data = wav
        self.sample_rate = sr

        self.start = 0
        self.length = 60

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
        grid.addWidget(QLabel(10*"dicks\n"), 0, 0)
        grid.addWidget(QLabel("dicks"), 0, 1)
        grid.addWidget(QLabel("dicks"), 0, 2)
        grid.addWidget(QLabel("dicks"), 0, 3)

        # Row 1 - db/time graph
        av = AudioView(self.wav_data, self.sample_rate, parent=self)
        grid.addWidget(av, 1, 0, 1, 4)

        # Row 2 - timeline
        timeline = Timeline()
        grid.addWidget(timeline, 2, 0, 1, 4)

        # Relative Row Heights
        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)


        main_widget = QWidget()
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)

    def load_audiofile(self, filepath):
        if not os.path.exists(filepath):
            QMessageBox.warning(self, "File does not exist", "{} Does not exists".format(filepath))
            return
        self.project['filepath'] = filepath
        wav, sr  = librosa.load(filepath, sr=None)
        self.sound_data = wav
        self.sample_rate = sr
        self.project['song_length'] = 1000 * (sr/wav.shape[0])

    def new_project(self):

        # Open file dialog to pick a song
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getOpenFileName(self, "Import a Song", "","All Files (*)", options=options)
        if filepath:
            self.project = {}
            self.load_audiofile
            # self.load_project(filename)


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
            self.project = json.load(filename)
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
            if self.filename is not None:
                with open(self.filename, 'w') as f:
                    json.dump(self.project, f)
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

class AudioView(QWidget):
    def __init__(self, audio_data, sample_rate, parent=None):
        # super(AudioView).__init__(parent)
        QWidget.__init__(self, parent)
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.song_duration = self.audio_data.shape[0]/self.sample_rate 
        self.max_amplitude = max(self.audio_data) * 1.1
        self.start = 0
        self.length = 60
        # Interval between graphed samples (Because graphing all of them takes a long time)
        self.interval = 1 # miliseconds
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(46, 70, 125))
        self.setPalette(p)


    def plot_wav(self):
        plot_width = self.geometry().width()
        plot_height = self.geometry().height()

        center = int(plot_height / 2.0)

        # Convert Time to Samples
        start_sample = self.start * self.sample_rate
        num_samples = self.length * self.sample_rate
        end_sample = start_sample + num_samples
        if end_sample > self.audio_data.shape[0]:
            end_sample = self.audio_data.shape[0]
            num_samples = end_sample - start_sample
        num_samples_skip = int((self.interval/1000.0) * self.sample_rate)

        processed_num_samples = int(num_samples/num_samples_skip)
        # print("Processing Song - {} Samples".format(processed_num_samples))        
        self.max_amplitude = 2*max(self.audio_data[start_sample:end_sample])
        index = 0.0
        for i in range(start_sample, end_sample, num_samples_skip):
            x = (index/processed_num_samples) * plot_width
            y = ((self.audio_data[i]/self.max_amplitude) * plot_height) + center
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