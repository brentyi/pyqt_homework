from PyQt5.QtWidgets import QBoxLayout, QWidget, QComboBox, QDockWidget, QSlider, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

from .fancy_slider import FancySlider


class ControlDock(QDockWidget):
    """
    Qt widget containing a dropdown for selecting the function to plot and
    modifying its parameters.
    """

    def __init__(self, function_list, plot_canvas, parent=None):
        super().__init__(parent)

        # Prevent closing
        self.setFeatures(QDockWidget.DockWidgetMovable |
                         QDockWidget.DockWidgetFloatable)

        # Initialize layout
        contents = QWidget()
        layout = QBoxLayout(QBoxLayout.LeftToRight, contents)
        layout.setContentsMargins(10, 0, 10, 20)
        self.setWidget(contents)

        # Add function selection dropdown to layout
        label_combobox = QLabel()
        label_combobox.setText("<b>Function:</b>")
        layout.addWidget(label_combobox)
        layout.setAlignment(label_combobox, Qt.AlignCenter)
        combobox_function = QComboBox()

        # Add functions to dropdown, create map so we can associate values back
        # with original function objects
        self._function_map = {}
        for function in function_list:
            item_text = f"{function.name}: {function.description}"
            combobox_function.addItem(item_text)
            self._function_map[item_text] = function
        layout.addWidget(combobox_function)

        # Add "A" parameter slider to layout
        slider_a = FancySlider("A", -10.0, 10.0, 20)
        layout.addWidget(slider_a)

        # Add "B" parameter slider to layout
        slider_b = FancySlider("B", -10.0, 10.0, 20)
        layout.addWidget(slider_b)

        # Event handlers: update the plot whenever a relevant change is made
        combobox_function.currentTextChanged.connect(self.updatePlot)
        slider_a.valueChanged.connect(self.updatePlot)
        slider_b.valueChanged.connect(self.updatePlot)

        # Event handler: rotate our dock based on where the user puts it
        self.dockLocationChanged.connect(self.updateDockOrientation)

        # Save some elements for later access
        self._layout = layout
        self._combobox_function = combobox_function
        self._slider_a = slider_a
        self._slider_b = slider_b
        self._plot_canvas = plot_canvas

        # Render initial state
        self.updatePlot()

    @pyqtSlot()
    def updatePlot(self):
        # Update plot
        function = self._function_map[self._combobox_function.currentText()]
        function.a = self._slider_a.value()
        function.b = self._slider_b.value()

        self._plot_canvas.plotFunction(function)

    @pyqtSlot(Qt.DockWidgetArea)
    def updateDockOrientation(self, area):
        # Rotate layout based on where we're docked
        if area in (Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea):
            self.setMaximumWidth(120)
            self.setMaximumHeight(2560)
            self._layout.setDirection(QBoxLayout.TopToBottom)
            self._slider_a.setOrientation(Qt.Vertical)
            self._slider_b.setOrientation(Qt.Vertical)
        else:
            self.setMaximumWidth(2560)
            self.setMaximumHeight(120)
            self._layout.setDirection(QBoxLayout.LeftToRight)
            self._slider_a.setOrientation(Qt.Horizontal)
            self._slider_b.setOrientation(Qt.Horizontal)
