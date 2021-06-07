import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLineEdit,
    QTextEdit,
    QFormLayout,

)

class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.setGeometry(100,100,400,300)
        self.setWindowTitle('test')

        edit1 = QLineEdit()
        edit1.setValidator(QIntValidator())#只接收整数
        edit1.setMaxLength(4)#最多四位
        edit1.setAlignment(Qt.AlignCenter)#对齐样式
        edit1.setFont(QFont("Arial",20))#设置字体

        edit2 = QLineEdit()
        edit2.setValidator(QDoubleValidator(0.99,99.99,2))#最多两位小数

        edit3 = QLineEdit()
        edit3.setInputMask("+99_9999_999999")#设定输入的格式

        edit4 = QLineEdit()
        edit4.textChanged.connect(self.textchanged)#文本修改事件

        edit5 = QLineEdit()
        edit5.setEchoMode(QLineEdit.Password) #设定显示模式为密码
        edit5.editingFinished.connect(self.enterPress) #编辑结束事件

        edit6 = QLineEdit("Hello World")
        edit6.setReadOnly(True) #默认文本，且为只读

        self.edit7 = QTextEdit()
        self.edit7.textChanged.connect(self.text7changed)

        flo = QFormLayout()#表单布局
        flo.addRow("只能输入整数", edit1)
        flo.addRow("只能输入两位小数", edit2)
        flo.addRow("设定输入的格式", edit3)
        flo.addRow("文本修改事件", edit4)
        flo.addRow("设定显示模式为密码", edit5)
        flo.addRow("默认文本且只读", edit6)
        flo.addRow("QTextEdit使用示例", self.edit7)#解决中文显示乱码问题

        self.setLayout(flo)

    def textchanged(self,text):
        print("contents of text box: " + text)

    def text7changed(self):
        data = self.edit7.toPlainText() #不转换输入中文会报错！！！！！！！
        print("contents of text box: \n" + data)
        print(type(self.edit7.toPlainText()))

    def enterPress(self):
        print("edited")

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 每个Pyqt的程序都必须创建一个application对象，application在 QtGui 模块中，sys.argv 参数是命令行中的一组参数。
    w = window()
    w.show()
    sys.exit(app.exec_())  # app.exec_()其实就是QApplication的方法，原来这个exec_()方法的作用是“进入程序的主循环直到exit()被调用”，如果没有这个方法，运行的时候窗口会闪退。
