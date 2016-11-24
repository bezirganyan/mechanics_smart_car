from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import numpy as np
import pyqtgraph as pg

class Car:
    __maxVelocity = None;
    __curVelocity = None;
    __maxAcceleration = None;
    __distance = None;
    __length = None;
    __action = None;
    __time = None;

    def setValues(self, w):
        self.__maxVelocity = w.textMaxVel.text();
        self.__curVelocity = w.textCurVel.text();
        self.__maxAcceleration = w.textMaxAcc.text();
        self.__time = w.textTime.text();
        self.__distance = w.textDistance.text();
        self.__length = w.textLength.text();

    def getResults(self):
        V0 = float(self.__curVelocity)*1000/3600; #Initial Velocity
        Vf = float(self.__maxVelocity)*1000/3600; #Final (maximum) Velocity
        Af = float(self.__maxAcceleration);
        d = float(self.__distance);
        l = float(self.__length);
        t = float(self.__time);
        t_lim = None;
        result = [];
        temp_a = [];
        temp_x = [];
        for a in np.arange(-Af, Af, 0.1):
            a = float("{0:.1f}".format(a));
            if (a < 0):
                x = - float("{0:.1f}".format((V0*V0)/(2*a)));
            else:
                if (a != 0):
                    t_lim = (Vf - V0)/a;
                    if (t_lim < t):
                        x = (V0*t_lim)+(a*t_lim*t_lim)/2 + Vf*(t - t_lim);
                        x = float("{0:.1f}".format(x))
                    else:
                        x = float("{0:.1f}".format(V0*t + a*t*t/2));
                else:
                    x = float("{0:.1f}".format(V0*t + a*t*t/2));
            temp_a.append(a);
            temp_x.append(x);
        result.append(temp_a);
        result.append(temp_x);

        return result;

class Window(QtGui.QWidget):
    def confirm(self):
        self.car.setValues(self);
        self.plot(self.car.getResults())

    def plot(self, res):
        print(res)
        a = np.array(res[0]);
        s = np.array(res[1]);
        d = float(self.textDistance.text());
        l = float(self.textLength.text());
        self.pt.clear();
        self.pt.getPlotItem().addLine(x = 0,movable =False,pen = {'color':"r"})
        self.pt.getPlotItem().addLine(y = d,movable =False,pen = {'color':"g"})
        self.pt.getPlotItem().addLine(y = d+l,movable =False,pen = {'color':"b"})
        self.pt.getPlotItem().addItem(pg.PlotCurveItem(x = a, y = s, pen='b'));

    def createInputs(self):
        self.textMaxVel = QtGui.QLineEdit();
        self.textMaxVel.setPlaceholderText('Maximum Velocity (km/h)');
        self.textMaxVel.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textCurVel = QtGui.QLineEdit();
        self.textCurVel.setPlaceholderText('Current Velocity (km/h)');
        self.textCurVel.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textMaxAcc = QtGui.QLineEdit();
        self.textMaxAcc.setPlaceholderText('Maximum Acceleration (m/h^2)');
        self.textMaxAcc.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textTime = QtGui.QLineEdit();
        self.textTime.setPlaceholderText('Time remaining (s)');
        self.textTime.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textDistance = QtGui.QLineEdit();
        self.textDistance.setPlaceholderText('Distance to the Interaction (m)');
        self.textDistance.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textLength = QtGui.QLineEdit();
        self.textLength.setPlaceholderText('Length of the Interaction (m)');
        self.textLength.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textMaxVel.setStyleSheet("width: 150px;");

    def createLabels(self):
        pass;
    def createButtons(self):
        self.btn = QtGui.QPushButton('Confirm');

    def addCreatedWidgets(self):
        indY = 0;
        self.layout.addWidget(self.textMaxVel, indY, 0, 1, 3);
        indY += 1;
        self.layout.addWidget(self.textCurVel, indY, 0, 1, 3);
        indY += 1;
        self.layout.addWidget(self.textMaxAcc, indY, 0, 1, 3);
        indY += 1;
        self.layout.addWidget(self.textTime, indY, 0, 1, 3);
        indY += 1;
        self.layout.addWidget(self.textDistance, indY, 0, 1, 3);
        indY += 1;
        self.layout.addWidget(self.textLength, indY, 0, 1, 3);
        indY += 1;

        self.layout.addWidget(self.pt, 0, 3, 10, 1);
        self.layout.addWidget(self.btn, 10, 0, 1, 3);
        self.connect(self.btn, SIGNAL("clicked()"), self.confirm);

    def drawWindow(self):
        pg.setConfigOption('background', 'w');
        pg.setConfigOptions(antialias=True);
        self.w = QtGui.QWidget();
        self.w.setWindowTitle('Smart Car');
        self.pt = pg.PlotWidget();
        self.pt.getPlotItem().setLabel('left', text = 'Distance (m)')
        self.pt.getPlotItem().setLabel('bottom', text = 'Acceleration (m/s^2)')

        self.layout = QtGui.QGridLayout();
        self.w.setLayout(self.layout);

        self.createInputs();
        self.createButtons();
        self.createLabels();
        self.addCreatedWidgets();

        self.w.setFocus();
        self.w.show();
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.car = Car();
        self.drawWindow();

app = QtGui.QApplication([]);
window = Window();
app.exec_()
