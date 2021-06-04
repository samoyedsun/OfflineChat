import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('QComboBox的使用')

        self.lb1 = QLabel('')
        self.cb = QComboBox()
        self.cb.addItem('C')
        self.cb.addItem('C++')
        self.cb.addItems(['Java','Python','C#'])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        layout = QVBoxLayout()
        layout.addWidget(self.cb)
        layout.addWidget(self.lb1)
        self.setLayout(layout)

    def selectionchange(self,i):
        self.lb1.setText(self.cb.currentText())
        print('Items in the list are:')
        for count in range(self.cb.count()):
            print('item'+str(count)+'='+self.cb.itemText(count))
            print('Current index',i,'selection changed',self.cb.currentText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Win()
    form.show()
    sys.exit(app.exec_())