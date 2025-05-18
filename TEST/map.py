import sys
import io
import matplotlib
import numpy
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore,QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
class MatPlotLibExample(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig=Figure(figsize=(width, height),dpi=dpi)
        self.axes=fig.add_subplot(111)
        super()._init_(fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *ars, **kwargs):
        super().__init__(*args,**kwargs)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()

app = QtWidgets.QApplication(sys.argv)
w=MainWindow()
app,exec_()
      