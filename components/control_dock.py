from PyQt5.QtWidgets import QBoxLayout, QWidget, QComboBox, QDockWidget, QSlider, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt


class ControlDock(QDockWidget):
    def __init__(self, function_list, plot_canvas, parent=None):
        # Call superclass constructor
        QDockWidget.__init__(self, parent)

        # Initialize layout
        contents = QWidget()
        layout = QBoxLayout(QBoxLayout.LeftToRight, contents)
        layout.setContentsMargins(10, 0, 10, 20)
        self.setWidget(contents)

        # Add function selector to layout
        combobox_function = QComboBox()
        self.function_map = {}
        for function in function_list:
            combobox_function.addItem(function.name)
            self.function_map[function.name] = function
        combobox_function.currentTextChanged.connect(self.update_plot)
        layout.addWidget(combobox_function)

        # Add "A" slider to layout
        slider_a = FancySliderWidget("A", -10.0, 10.0, 20)
        slider_a.valueChanged.connect(self.update_plot)
        layout.addWidget(slider_a)

        # Add "B" slider to layout
        slider_b = FancySliderWidget("B", -10.0, 10.0, 20)
        slider_b.valueChanged.connect(self.update_plot)
        layout.addWidget(slider_b)

        # Store some elements for later access
        self.layout = layout
        self.combobox_function = combobox_function
        self.slider_a = slider_a
        self.slider_b = slider_b
        self.plot_canvas = plot_canvas

        # Render initial state
        self.update_plot()

    @pyqtSlot()
    def update_plot(self):
        # Update plot
        function = self.function_map[self.combobox_function.currentText()]
        function.a = self.slider_a.value()
        function.b = self.slider_b.value()

        self.plot_canvas.plot(function)


class FancySliderWidget(QWidget):
    valueChanged = pyqtSignal([float])

    def __init__(self, name, min_val=0, max_val=100, ticks=100, parent=None):
        QWidget.__init__(self, parent)

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
