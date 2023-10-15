import pyqtgraph as pg

uiclass, baseclass = pg.Qt.loadUiType("graph.ui")
class PlotterWindow(uiclass, baseclass):

    def __init__(self, x, y):
        super().__init__()
        self.setupUi(self)
        self.plot(x, y)
        self.setWindowTitle("Data Plotter")
    
    def plot(self, x, y):
        self.graphWidget.clear()
        pen = pg.mkPen(color=(255, 0, 0))

        time_labels = [
            # Generate a list of tuples (x_value, x_label)
            (m, x[m])
            for m in range(len(x))
        ]
        self.graphWidget.plot(range(len(x)), y, pen=pen, labels=time_labels)
        ax = self.graphWidget.getAxis('bottom')
        ax.setTicks([time_labels])