# region imports
from Car_GUI import Ui_Form
import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from QuarterCarModel import CarController

# these imports are necessary for drawing a matplot lib graph on my GUI
# no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# endregion

class SchematicView(qtw.QGraphicsView):
    class Spring(qtw.QGraphicsLineItem):
        def __init__(self, startX, startY, endX, endY, pen=None):
            super().__init__(startX, startY, endX, endY)
            self.setFlag(qtw.QGraphicsItem.ItemIsSelectable, True)
            if pen is not None:
                self.setPen(pen)

        def addToScene(self, scene):
            scene.addItem(self)

    class Dashpot(qtw.QGraphicsLineItem):
        def __init__(self, startX, startY, endX, endY, pen=None):
            super().__init__(startX, startY, endX, endY)
            self.setFlag(qtw.QGraphicsItem.ItemIsSelectable, True)
            if pen is not None:
                self.setPen(pen)

        def addToScene(self, scene):
            scene.addItem(self)

    def __init__(self):
        super().__init__()
        self.setScene(qtw.QGraphicsScene())

        # Add spring and dashpot to the scene
        self.addSpring(50, 50, 100, 100, qtg.QPen(qtc.Qt.black))
        self.addDashpot(150, 50, 200, 100, qtg.QPen(qtc.Qt.black))

    def addSpring(self, startX, startY, endX, endY, pen=None):
        spring = self.Spring(startX, startY, endX, endY, pen)
        spring.addToScene(self.scene())

    def addDashpot(self, startX, startY, endX, endY, pen=None):
        dashpot = self.Dashpot(startX, startY, endX, endY, pen)
        dashpot.addToScene(self.scene())


# Usage example:
schematic_view = SchematicView()
schematic_view.addSpring(50, 50, 100, 100, qtg.QPen(qtc.Qt.black))
schematic_view.addDashpot(150, 50, 200, 100, qtg.QPen(qtc.Qt.black))
class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        Main window constructor.
        """
        super().__init__()
        # call setupUi from Ui_Form parent
        self.setupUi(self)

        # setup car controller
        input_widgets = (self.le_m1, self.le_v, self.le_k1, self.le_c1, self.le_m2, self.le_k2, self.le_ang, \
                         self.le_tmax, self.chk_IncludeAccel)
        display_widgets = (self.gv_Schematic, self.chk_LogX, self.chk_LogY, self.chk_LogAccel, \
                           self.chk_ShowAccel, self.lbl_MaxMinInfo, self.layout_horizontal_main)

        # instantiate the car controller
        self.controller = CarController((input_widgets, display_widgets))

        # connect signal to slots
        self.btn_calculate.clicked.connect(self.controller.calculate)
        self.pb_Optimize.clicked.connect(self.doOptimize)
        self.chk_LogX.stateChanged.connect(self.controller.doPlot)
        self.chk_LogY.stateChanged.connect(self.controller.doPlot)
        self.chk_LogAccel.stateChanged.connect(self.controller.doPlot)
        self.chk_ShowAccel.stateChanged.connect(self.controller.doPlot)
        self.show()

    def doOptimize(self):
        app.setOverrideCursor(qtc.Qt.WaitCursor)
        self.controller.OptimizeSuspension()
        app.restoreOverrideCursor()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Quarter Car Model')
    sys.exit(app.exec())
