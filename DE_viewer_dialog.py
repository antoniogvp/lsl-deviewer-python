from qtpy import QtGui, QtCore, QtWidgets, uic
 
import os

qtCreatorFile = "DE_viewer_dialog.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(os.path.dirname(__file__),qtCreatorFile))
 
class DialogDE(QtWidgets.QDialog, Ui_MainWindow):
 
    def __init__(self, listStreams):
        super(DialogDE, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        for stream in listStreams:
            chkBoxItem = QtWidgets.QListWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            chkBoxItem.setText(stream)
            self.listStreams.addItem(chkBoxItem)
        self.samplingRateEdit.setValidator(QtGui.QIntValidator(0, 2147483647))
            
    def returnWindowParameters(self):
        sampling_rate = self.samplingRateEdit.text()
        checkedItems = []
        for index in range(self.listStreams.count()):
            if self.listStreams.item(index).checkState() == QtCore.Qt.Checked:
                checkedItems.append(index)
        return checkedItems, sampling_rate
    
    def checkLineEditPattern(self):
        parameters_ok = True
        
        if self.samplingRateEdit.text() == "":
            parameters_ok = False
        
        if parameters_ok is False:
            QtWidgets.QMessageBox.critical(None,'Error','Sampling rate was not correctly specified.',QtWidgets.QMessageBox.Cancel)
                
        return parameters_ok
            
    def showErrorNoStreams(self):
        QtWidgets.QMessageBox.critical(None,'Error','No online streams were found. Please make sure devices are correctly connected and linked.',QtWidgets.QMessageBox.Cancel)
    
    def showErrorNoStreamSelected(self):
        QtWidgets.QMessageBox.critical(None,'Error','No stream was selected.',QtWidgets.QMessageBox.Cancel)
 
#if __name__ == '__main__':
#    app = QtWidgets.QApplication(sys.argv)
#    dialog = DialogDE(["test","2"])
#    dialog.exec_()
#    #sys.exit(dialog.exec_())
#    items = dialog.returnWindowParameters()