#!/usr/bin/env python3

import sys
import signal
import argparse

import widgets
import functions

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class PlotToolApp(QMainWindow):
    def __init__(self, function_list):
        super().__init__()
        self.initUI(function_list)

    def initUI(self, function_list):
        # Window setup
        self.setWindowTitle("Plotting Tool")
        self.setGeometry(100, 100, 1280, 720)

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

    # Create plottable function objects
    function_list = [
        functions.Sine(),
        functions.Polynomial(),
        functions.Mystery()
    ]
    function_names = [f.name.lower() for f in function_list]

    # Parse function list argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        help="Comma-separated list of functions. Options are: " +
        ",".join(function_names),
        type=str)
    args = parser.parse_args()

    if args.list:
        # If argument exists, filter out function list
        # Otherwise, all functions are included by default
        function_list = [f for f in function_list if f.name.lower()
                         in args.list.split(",")]

    # Run application
    app = QApplication(sys.argv)
    ex = PlotToolApp(function_list)
    sys.exit(app.exec_())
