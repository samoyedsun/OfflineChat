from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox
)
import sys
import moduleConfig as ModuleConfig
import moduleWechat as ModuleWechat
import moduleSClient as ModuleSClient
import moduleQrcode as ModuleQrcode

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle(ModuleConfig.APP_TITLE + '  Version:' + ModuleConfig.APP_VERSION)
        self.setGeometry(300, 300, 700, 700)

        labelGame = QLabel(self)
        labelGame.setText('游戏:')
        labelGame.setStyleSheet('''
            font-size: 16px;
        ''')
        labelGame.move(10, 15)

        labelPlatform = QLabel(self)
        labelPlatform.setText('平台:')
        labelPlatform.setStyleSheet('''
            font-size: 16px;
        ''')
        labelPlatform.move(10, 60)

        labelAccount = QLabel(self)
        labelAccount.setText('账号:')
        labelAccount.setStyleSheet('''
            font-size: 16px;
        ''')
        labelAccount.move(10, 105)

        labelPassword = QLabel(self)
        labelPassword.setText('密码:')
        labelPassword.setStyleSheet('''
            font-size: 16px;
        ''')
        labelPassword.move(10, 150)

        labelServerName = QLabel(self)
        labelServerName.setText('区服:')
        labelServerName.setStyleSheet('''
            font-size: 16px;
        ''')
        labelServerName.move(10, 195)
        
        qcbGameList = QComboBox(self)
        qcbGameList.addItems(ModuleConfig.GAME_LIST)
        qcbGameList.move(50, 10)
        qcbGameList.currentIndexChanged.connect(self.selectionChange)

        qcbGameList = QComboBox(self)
        qcbGameList.addItems(ModuleConfig.PLATFORM_LIST)
        qcbGameList.move(50, 55)
        qcbGameList.currentIndexChanged.connect(self.selectionChange)

        leAccount = QLineEdit(self)
        leAccount.setPlaceholderText("请输入您的账号!")
        leAccount.move(50, 105)

        lePassword = QLineEdit(self)
        lePassword.setPlaceholderText("请输入您的密码!")
        lePassword.move(50, 150)

        leServerName = QLineEdit(self)
        leServerName.setPlaceholderText("请输入您所在的区服!")
        leServerName.move(50, 195)

        buttonLogin = QPushButton(self)
        buttonLogin.setText('登陆')
        buttonLogin.move(10, 300)
        buttonLogin.clicked.connect(self.login)

    def selectionChange(self, i):
        print('选择了:', i)

    def login(self):
        headerInfo = {
            'channel': ModuleConfig.MHZX_CHANNEL,
            'offerid': ModuleConfig.MHZX_OFFERID,
            'platform': ModuleConfig.MHZX_PLATFORM,
            'os': ModuleConfig.MHZX_OS,
            'grantType': ModuleConfig.MHZX_GRANT_TYPE,
            'grayType': ModuleConfig.MHZX_GRAY_TEST,
            'localIP': ModuleConfig.MHZX_LOCAL_IP,
            'deviceInfo': ModuleConfig.MHZX_DEVICE_INFO
        }
        wechatObj = ModuleWechat.Wechat(ModuleConfig.MHZX_APPID, ModuleConfig.MHZX_MSDK_KEY, headerInfo)
        qrcodeInfo = wechatObj.getQrcodeInfo()
        if not qrcodeInfo:
            return False
        qrcodeBinary = qrcodeInfo['qrcodebinary']
        qrcodeDetail = qrcodeInfo['qrcodedetail']
        qrcodeDialog = ModuleQrcode.Qrcode(qrcodeBinary, qrcodeDetail)
        loginInfo = qrcodeDialog.showQrcode(wechatObj)
        if not loginInfo:
            return False
        sclientObj = ModuleSClient.SClient(ModuleConfig.MHZX_SERVER_NAME, ModuleConfig.MHZX_SERVER_PORT)
        serverMap = sclientObj.getServerMap()
        print(loginInfo)
        print(serverMap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())