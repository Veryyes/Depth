from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

import math

class Timeline(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,300,192)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.red)
        size = self.size()
        for x in range(-1000,1000):
            qp.drawPoint(x, 500*math.sin(x))
        qp.end()