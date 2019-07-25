from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import numpy as np

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Initialize FigureCanvas
        FigureCanvas.__init__(self, plt.Figure())
        self.setParent(parent)

    def plot(self, function):
        # Clear figure
        self.figure.clf()

        # Plot
        data_x = np.linspace(-10.0, 10.0, 1000)
        data_y = np.array([function(x) for x in data_x])
        ax = self.figure.add_subplot(111)
        ax.plot(data_x, data_y)

        # Set title and labels
        ax.set_title(
            function.description +
            ", A = {}, B = {}".format(
                *np.round((function.a, function.b), 2)
            )
        )
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        # Render
        self.draw()

