from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import numpy as np


class PlotCanvas(FigureCanvas):
    """Qt widget that plots an arbitrary function via matplotlib."""

    def __init__(self, parent=None):
        # Initialize FigureCanvas
        super().__init__(plt.Figure())
        self.setParent(parent)

    def plotFunction(self, function):
        # Clear figure
        self.figure.clf()

        # Plot
        data_x = np.linspace(-10.0, 10.0, 1000)
        data_y = np.array([function(x) for x in data_x])
        ax = self.figure.add_subplot(111)
        ax.plot(data_x, data_y)

        # Set title and labels
        ax.set_title(
            f"{function.description}, A = {function.a:.2}, B = {function.b:.2}"
        )
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        # Render
        self.draw()
