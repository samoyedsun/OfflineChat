import sys
from PySide6 import QtWidgets, QtGui, QtCore

import moduleConfig
import moduleWechat as ModuleWechat

appVersion = ' Version:0.0.1' + '    PySide6 Version:' + QtCore.__version__

# 定义主界面
def mainWindow():
    # 我事实上不太明白干嘛要这一句话，只是pyqt窗口的建立都必须调用QApplication方法
    app = QtWidgets.QApplication(sys.argv)
    # 新建一个窗口，名字叫做w
    w = QtWidgets.QWidget()
    # 定义w的大小
    w.setGeometry(300, 300, 700, 700)
    # 给w一个标题
    w.setWindowTitle('私聊器' + appVersion)
    # 设置透明度以及风格
    w.setWindowOpacity(0.8)
    w.setStyleSheet("""
        background: #000000;
    """)
    # 在窗口中创建一个按钮
    b1 = QtWidgets.QPushButton(w)
    b1.setText("登陆")
    b1.setStyleSheet("""
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 1px;
        padding-bottom: 1px;
        border:1px solid #FFFF00;
        border-radius: 5px;
        background: #00CC00;
        color: #000000;
    """)
    b1.move(50, 50)

    def login():
        headerInfo = {
            'channel': moduleConfig.MHZX_CHANNEL,
            'offerid': moduleConfig.MHZX_OFFERID,
            'platform': moduleConfig.MHZX_PLATFORM,
            'os': moduleConfig.MHZX_OS,
            'grantType': moduleConfig.MHZX_GRANT_TYPE,
            'grayType': moduleConfig.MHZX_GRAY_TEST,
            'localIP': moduleConfig.MHZX_LOCAL_IP,
            'deviceInfo': moduleConfig.MHZX_DEVICE_INFO
        }
        wechatObj = ModuleWechat.Wechat(moduleConfig.MHZX_APPID, moduleConfig.MHZX_MSDK_KEY, headerInfo)
        qrcodeInfo = wechatObj.getQrcodeInfo()
        if not qrcodeInfo:
            return False
        qrcodebinary = qrcodeInfo['qrcodebinary']
        qrcodedetail = qrcodeInfo['qrcodedetail']
        image_qrcode = QtGui.QPixmap()
        image_qrcode.loadFromData(qrcodebinary)

        dialog = QtWidgets.QDialog()
        def closeDialog():
            dialog.accept()
        l1 = QtWidgets.QLabel(dialog)
        l1.setPixmap(image_qrcode)
        l1.move(0, 0)

        l2 = QtWidgets.QLabel(dialog)
        def setL2Attr(content, styleSheet):
            l2.setText(content)
            l2.setStyleSheet(styleSheet)
        setL2Attr(qrcodedetail, """
            font-size: 18px;
            background-color: #660BAB;
        """)
        l2.move(0, 470)
        
        dialog.setWindowTitle("扫码登陆")
        dialog.resize(470, 500)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)

        wechatObj.checkQrcodeStatus(setL2Attr, closeDialog)
        
        dialog.exec()
        # 这一行要加，手动关闭dialog的时候需要终止检测二维码状态的线程
        wechatObj.setCheckRuning(False)
        print(wechatObj.getLoginInfo())
    b1.clicked.connect(login)

    # 显示整个窗口
    w.show()

    # 退出整个app
    app.exit(app.exec())

# 创建主界面
mainWindow() 
