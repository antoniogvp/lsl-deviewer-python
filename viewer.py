#import numpy as np
from pylsl import StreamInlet, resolve_stream, local_clock
from DE_viewer_dialog import DialogDE
from qtpy import QtGui, QtCore, QtWidgets, uic
import numpy as np

import os

qtCreatorFile = "viewer.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(os.path.dirname(__file__),qtCreatorFile))

def classifyStreamInlet(streams):
    listStreams = []
    for stream in streams:
        listStreams.append(StreamInlet(stream).info().name())
    return listStreams

class Viewer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, selectedStreams, streams, update_rate):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.comboBox_src.currentIndexChanged.connect(self.changeDisplayedStream)
        self.inlet = []
        self.storedData = []
        self.storedData.append([]) # All events list
        self.selectedStream = 0 # By default events from all sources are displayed
        self.dataAcquisition = True # By default data acquisition is active 
        self.update_rate = update_rate
        for num in selectedStreams:
            self.comboBox_src.addItem(StreamInlet(streams[num]).info().name())
            self.inlet.append(StreamInlet(streams[num], max_buflen=10))
            self.storedData.append([]) # Single event list
        self.configureTable()
        self.action_buffering_time.triggered.connect(self.changeBufferingTime)
        self.bufferTime = 100
        self.StopButton.setFocus()
        self.StopButton.clicked.connect(self.setStopResume)
        self.CloseButton.clicked.connect(self.stopAndClose)
        self.configureTimers()
        
    def configureTimers(self):
        self.timerData = QtCore.QTimer()
        self.timerData.timeout.connect(self.updateData)
        self.timerData.start(1000.0/self.update_rate)
                
        self.timerBuffer = QtCore.QTimer()
        self.timerBuffer.timeout.connect(self.updateBuffer)
        self.timerBuffer.start(1000.0)
        
    def configureTable(self):
        self.eventTable.horizontalHeader().setStretchLastSection(True)
        self.eventTable.setColumnWidth(0, 100)
        self.eventTable.setColumnWidth(1, 140)
        self.tableColorList = [QtCore.Qt.white, QtCore.Qt.yellow, QtCore.Qt.red,
                               QtCore.Qt.green,QtCore.Qt.magenta, QtCore.Qt.cyan]
    
    def changeBufferingTime(self,q):
        n, ok = QtWidgets.QInputDialog().getInt(self, "Maximum data buffering time",
                                 "Time to remove data from buffer [s]:", self.bufferTime, 1, 9999, 1)
        if ok:
            self.bufferTime = n
            
    def changeDisplayedStream(self, i):
        if self.selectedStream is not i:
            self.selectedStream = i
            self.eventTable.setRowCount(0) # delete all rows
            for event in self.storedData[i]:
                self.updateTable(event)
            
    def updateData(self):
        for stream in self.inlet:
            chunk, timestamps = stream.pull_chunk(timeout=0.0)
            if self.dataAcquisition is True:
                if timestamps:
                    ts = np.asarray(timestamps)
                    y = np.asarray(chunk)
                    
                    for elem in range(len(ts)):
                        event = []
                        event.append(stream.info().name())
                        event.append(float(ts[elem]))
                        event.append(str(y[elem,:]))
                        event.append(self.inlet.index(stream)%6)
                        self.storedData[0].insert(0,event)
                        self.storedData[self.inlet.index(stream)+1].insert(0,event)
                    
                        if self.selectedStream == 0 or self.inlet.index(stream)+1 == self.selectedStream:
                            self.updateTable(event)
    
    def updateTable(self, event):
        self.eventTable.insertRow (0)
        
        for n in range(len(event)-1):
            elem = QtWidgets.QTableWidgetItem(str(event[n]))
            elem.setFlags(elem.flags() & ~QtCore.Qt.ItemIsEditable)
            elem.setBackground(self.tableColorList[event[len(event)-1]])
            self.eventTable.setItem(0, n, elem)
            
    def updateBuffer(self):
        for s in self.storedData:
            for l in reversed(s):
                if (l[1] - local_clock()) <= - self.bufferTime:
                    s.remove(l)
                else:
                    break
            
        for rowIndex in reversed(range(self.eventTable.rowCount())):
            ts = self.eventTable.item(rowIndex, 1).text()
            if (float(ts) - local_clock()) <= - self.bufferTime:
                self.eventTable.removeRow(rowIndex)
            else:
                break
    
    def setStopResume(self):
        self.dataAcquisition = not(self.dataAcquisition)
        
        if self.dataAcquisition is True:
            self.StopButton.setText("Stop")
        else:
            self.StopButton.setText("Resume")
            
    def stopAndClose(self):
        self.close()
        
def Start():
    streams = resolve_stream()
    
    listStreams = classifyStreamInlet(streams)
    dialog = DialogDE(listStreams)

    if(len(listStreams) == 0):
        dialog.showErrorNoStreams()
    
    else:
        if dialog.exec_() and dialog.checkLineEditPattern():
            selectedStreams, update_rate = dialog.returnWindowParameters()
            
            if len(selectedStreams) == 0:
                dialog.showErrorNoStreamSelected()
            else:
                v = Viewer(selectedStreams, streams, int(update_rate))
                v.show()
        else:
            print("Window was not created.")
    return v
        
def main():
    v = Start()
    import sys
    if (((sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION')) ):
        QtWidgets.QApplication.instance().exec_()
    return v

if __name__ == '__main__':
    import sys
    v = Start()
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    if (((sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION')) ):
        app.instance().exec_()
    sys.exit(0)
    