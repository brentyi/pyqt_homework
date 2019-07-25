#!/usr/bin/env python3

import sys
import signal

import widgets
import functions

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle("Plotting Tool")
        self.setGeometry(100, 100, 1280, 720)

        # Function list
        function_list = [
            functions.Sine(),
            functions.Polynomial(),
            functions.Mystery()
        ]

        # Add function plot
        plot_canvas = widgets.PlotCanvas()
        self.setCentralWidget(plot_canvas)

        # Add control dock
        dock = widgets.ControlDock(function_list, plot_canvas, self)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        # Show app
        self.show()


if __name__ == '__main__':
    # Exit on CTRL + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Run application
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
