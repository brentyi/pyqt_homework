from PyQt5.QtWidgets import QBoxLayout, QWidget, QComboBox, QDockWidget, QSlider, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt


class ControlDock(QDockWidget):
    def __init__(self, function_list, plot_canvas, parent=None):
        # Call superclass constructor
        super().__init__(parent)

        # Initialize layout
        contents = QWidget()
        layout = QBoxLayout(QBoxLayout.LeftToRight, contents)
        layout.setContentsMargins(10, 0, 10, 20)
        self.setWidget(contents)

        # Add function selector to layout
        label_combobox = QLabel()
        label_combobox.setText("<b>Function:</b>")
        layout.addWidget(label_combobox)
        layout.setAlignment(label_combobox, Qt.AlignCenter)

        combobox_function = QComboBox()
        self._function_map = {}
        for function in function_list:
            combobox_function.addItem(function.name)
            self._function_map[function.name] = function
        layout.addWidget(combobox_function)

        # Add "A" slider to layout
        slider_a = FancySliderWidget("A", -10.0, 10.0, 20)
        layout.addWidget(slider_a)

        # Add "B" slider to layout
        slider_b = FancySliderWidget("B", -10.0, 10.0, 20)
        layout.addWidget(slider_b)

        # Store some elements for later access
        self._layout = layout
        self._combobox_function = combobox_function
        self._slider_a = slider_a
        self._slider_b = slider_b
        self._plot_canvas = plot_canvas

        # Render initial state
        self.update_plot()

        # Event handlers
        combobox_function.currentTextChanged.connect(self.update_plot)
        slider_a.valueChanged.connect(self.update_plot)
        slider_b.valueChanged.connect(self.update_plot)
        self.dockLocationChanged.connect(self.update_dock_orientation)

    @pyqtSlot()
    def update_plot(self):
        # Update plot
        function = self._function_map[self._combobox_function.currentText()]
        function.a = self._slider_a.value()
        function.b = self._slider_b.value()

        self._plot_canvas.plot(function)

    @pyqtSlot(Qt.DockWidgetArea)
    def update_dock_orientation(self, area):
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


class FancySliderWidget(QWidget):
    valueChanged = pyqtSignal([float])

    def __init__(self, name, min_val=0, max_val=100, ticks=100, parent=None):
        super().__init__(parent)

        layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        # Create slider object
        slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setRange(0, ticks)
        slider.setValue(ticks * 0.6)
        slider.setSingleStep(1)
        slider.setPageStep(1)

        # Create labels
        name_label = QLabel()
        name_label.setText("<b>{}:</b>".format(name))

        val_label = QLabel()

        # Add labels and slider to layout
        layout.addWidget(name_label)
        layout.addWidget(slider)
        layout.addWidget(val_label)

        # Store some elements for later access
        self._name_label = name_label
        self._slider = slider
        self._val_label = val_label
        self._layout = layout

        # Elevate some slider properties; this lets us maintain a similar
        # interface as a normal QSlider object
        slider.valueChanged.connect(
            lambda: self.valueChanged.emit(
                self.value()))
        self.value = lambda: (slider.value() / ticks) * \
            (max_val - min_val) + min_val
        self.valueChanged.connect(val_label.setNum)

        # Render initial state
        self.valueChanged.emit(self.value())

    @pyqtSlot(Qt.Orientation)
    def setOrientation(self, orientation):
        self._slider.setOrientation(orientation)
        if orientation == Qt.Vertical:
            direction = QBoxLayout.TopToBottom
            alignment = Qt.AlignHCenter
        elif orientation == Qt.Horizontal:
            direction = QBoxLayout.LeftToRight
            alignment = Qt.AlignVCenter

        self._layout.setDirection(direction)
        for w in (self._name_label, self._slider, self._val_label):
            self._layout.setAlignment(w, alignment)
