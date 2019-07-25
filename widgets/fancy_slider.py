from PyQt5.QtWidgets import QBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt


class FancySlider(QWidget):
    """
    Qt widget that mimics the QSlider class, but adds some labels and scaling
    functionality.
    """
    valueChanged = pyqtSignal([float])

    def __init__(self, name, min_val=0, max_val=100, ticks=100, parent=None):
        super().__init__(parent)

        # Creat layout
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
        name_label.setText(f"<b>{name}:</b>")

        val_label = QLabel()

        # Add labels and slider to layout
        layout.addWidget(name_label)
        layout.addWidget(slider)
        layout.addWidget(val_label)

        # Save some elements for later access
        self._name_label = name_label
        self._slider = slider
        self._val_label = val_label
        self._layout = layout

        # Surface some slider properties; this lets us maintain a similar
        # interface to the normal QSlider object
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
        # Match QSlider.setOrientation() interface

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
