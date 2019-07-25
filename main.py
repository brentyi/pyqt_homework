#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QComboBox, QDockWidget, QSlider, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 1280, 720)

        # Add function plot
        plot_canvas = PlotCanvas()
        self.setCentralWidget(plot_canvas)

        # Add control dock
        dock = ControlDock(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        # Show app
        self.show()


class ControlDock(QDockWidget):
    def __init__(self, parent=None):
        # Call superclass constructor
        QDockWidget.__init__(self, parent)

        # Initialize layout
        contents = QWidget()
        layout = QBoxLayout(QBoxLayout.LeftToRight, contents)
        self.setWidget(contents)

        # Add function selector to layout
        combobox_function = QComboBox()
        combobox_function.addItem("motif")
        combobox_function.addItem("Windows")
        layout.addWidget(combobox_function)

        # Add "A" slider to layout
        slider_a = FancySliderWidget("A", -10.0, 10.0)
        layout.addWidget(slider_a)

        # Add "B" slider to layout
        slider_b = FancySliderWidget("B", -10.0, 10.0)
        layout.addWidget(slider_b)

        # Store some elements for later access
        self.layout = layout
        self.slider_a = slider_a
        self.slider_b = slider_b

    @pyqtSlot()
    def update_plot(self):
        print(self.slider_a.value())
        pass


class FancySliderWidget(QWidget):
    def __init__(self, name, min_val=0, max_val=100, ticks=100, parent=None):
        QWidget.__init__(self, parent)

        layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        # Create slider object
        slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setRange(0, ticks)
        slider.setValue(ticks / 2)

        # Create labels
        name_label = QLabel()
        name_label.setText("<b>{}:</b>".format(name))

        min_label = QLabel()
        min_label.setText(str(min_val))

        max_label = QLabel()
        max_label.setText(str(max_val))

        val_label = QLabel()
        val_label.setText(str((max_val - min_val) / 2.0 + min_val))

        # Add labels and slider to layout
        layout.addWidget(name_label)
        layout.addWidget(min_label)
        layout.addWidget(slider)
        layout.addWidget(max_label)

        # Elevate some slider properties; this lets us maintain a similar
        # interface as a normal QSlider object
        self.valueChanged = slider.valueChanged
        self.value = lambda: (slider.value() / ticks) * \
            (max_val - min_val) - min_val


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.plot(data, "r-")
        ax.set_title("PyQt Matplotlib Example")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
