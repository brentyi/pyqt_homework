#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

import numpy as np
import signal

import components
import functions

signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 1280, 720)

        # Function list
        function_list = [
            functions.Sine(),
            functions.Polynomial(),
            functions.Mystery()
        ]

        # Add function plot
        plot_canvas = components.plot_canvas.PlotCanvas()
        self.setCentralWidget(plot_canvas)

        # Add control dock
        dock = components.ControlDock(function_list, plot_canvas, self)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        # Show app
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
