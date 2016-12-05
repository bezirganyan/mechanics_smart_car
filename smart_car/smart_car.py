from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import numpy as np
import pyqtgraph as pg

class Car:
    __maxVelocity = None;
    __curVelocity = None;
    __maxAcceleration = None;
    __minAcceleration = None;
    __distance = None;
    __length = None;
    __action = None;
    __time = None;

    def setValues(self, w):
        self.__maxVelocity = w.textMaxVel.text();
        self.__curVelocity = w.textCurVel.text();
        self.__maxAcceleration = w.textMaxAcc.text();
        self.__minAcceleration = w.textMinAcc.text();
        self.__time = w.textTime.text();
        self.__distance = w.textDistance.text();
        self.__length = w.textLength.text();

    def getResults(self):
        V0 = float(self.__curVelocity)*1000/3600; #Initial Velocity
        Vf = float(self.__maxVelocity)*1000/3600; #Final (maximum) Velocity
        Af = float(self.__maxAcceleration);
        Amin = - abs(float(self.__minAcceleration));
        d = float(self.__distance);
        l = float(self.__length);
        t = float(self.__time);
        t_lim = None;
        result = [];
        temp_a_br = [];
        temp_a = [];
        temp_x_br = [];
        temp_x = [];
        for a in np.arange(Amin, Af, 0.1):
            a = float("{0:.1f}".format(a));
            if (a < 0): #in the case of breaking
                tmp = - (V0*V0)/(2*a);
                if (tmp <= d):  #to plot only the accelerations, which will help
                                #to break in time
                    temp_x_br.append(tmp);
                    temp_a_br.append(a);
            else:
                if (V0 > Vf or a == 0):
                    t_lim = t;
                else:
                    t_lim = (Vf - V0)/a;

                if (t_lim < t):
                    x = (V0*t_lim)+(a*t_lim*t_lim)/2 + Vf*(t - t_lim);
                else:
                    x = V0*t + a*t*t/2;
                temp_a.append(a);
                temp_x.append(x);
        result.append(temp_a);
        result.append(temp_x);
        result.append(temp_a_br);
        result.append(temp_x_br);

        return result;

class Window(QtGui.QWidget):
    def confirm(self):
        self.car.setValues(self);
        self.plot(self.car.getResults())

    def plot(self, res):
        a = np.array(res[0]);
        s = np.array(res[1]);
        a_br = np.array(res[2]);
        s_br = np.array(res[3]);
        d = float(self.textDistance.text());
        l = float(self.textLength.text());
        self.pt.clear();
        self.pt.getPlotItem().addLine(x = 0,movable =False,pen = {'color':"y"})
        self.pt.getPlotItem().addLine(y = d,movable =False,pen = {'color':"b"})
        self.pt.getPlotItem().addLine(y = d+l,movable =False,pen = {'color':"b"})
        self.pt.getPlotItem().addItem(pg.PlotCurveItem(x = a, y = s, \
            pen= {'color':"g"}));
        self.pt.getPlotItem().addItem(pg.PlotCurveItem(x = a_br, y = s_br, \
            pen= {'color':"r"}));

    def createInputs(self):
        self.textMaxVel = QtGui.QLineEdit();
        self.textMaxVel.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textCurVel = QtGui.QLineEdit();
        self.textCurVel.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textMaxAcc = QtGui.QLineEdit();
        self.textMaxAcc.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textMinAcc = QtGui.QLineEdit();
        self.textMinAcc.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textTime = QtGui.QLineEdit();
        self.textTime.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textDistance = QtGui.QLineEdit();
        self.textDistance.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textLength = QtGui.QLineEdit();
        self.textLength.setValidator(QtGui.QDoubleValidator(0.99,99.99,2));

        self.textMaxVel.setStyleSheet("max-width: 30px;");
        self.textCurVel.setStyleSheet("max-width: 30px;");
        self.textMaxAcc.setStyleSheet("max-width: 30px;");
        self.textMinAcc.setStyleSheet("max-width: 30px;");
        self.textTime.setStyleSheet("max-width: 30px;");
        self.textDistance.setStyleSheet("max-width: 30px;");
        self.textLength.setStyleSheet("max-width: 30px;");

    def createLabels(self):
        self.maxVelLabel = QtGui.QLabel('Maximum Velocity (km/h)')
        self.curVelLabel = QtGui.QLabel('Current Velocity (km/h)')
        self.maxAccLabel = QtGui.QLabel('Maximum Acceleration (m/s^2)')
        self.minAccLabel = QtGui.QLabel('Minimum Acceleration (m/s^2)')
        self.timeLabel = QtGui.QLabel('Time Remaining (s)')
        self.distanceLabel = QtGui.QLabel('Distance to the Interaction (m)')
        self.lengthLabel = QtGui.QLabel('Length of the Interaction (m)')

    def createButtons(self):
        self.btn = QtGui.QPushButton('Confirm');

    def addCreatedWidgets(self):
        indY = 0;
        self.layout.addWidget(self.maxVelLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textMaxVel, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.curVelLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textCurVel, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.maxAccLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textMaxAcc, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.minAccLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textMinAcc, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.timeLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textTime, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.distanceLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textDistance, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.lengthLabel, indY, 0, 1, 3);
        self.layout.addWidget(self.textLength, indY, 3, 1, 1);
        indY += 1;

        self.layout.addWidget(self.pt, 0, 4, 15, 1);
        self.layout.addWidget(self.btn, 15, 0, 1, 4);
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
