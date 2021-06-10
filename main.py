from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QTableView,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QLabel,
    QCheckBox,
    QComboBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import sys, json
import moduleConfig as ModuleConfig
import moduleWechat as ModuleWechat
import moduleGClient as ModuleGClient
import moduleSClient as ModuleSClient
import moduleQrcode as ModuleQrcode

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle(ModuleConfig.APP_TITLE)
        self.setFixedSize(800, 700)

        self.status = self.statusBar()
        self.status.showMessage(ModuleConfig.APP_VERSION)

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
        
        self.qcbGameList = QComboBox(self)
        self.qcbGameList.addItems(ModuleConfig.GAME_LIST)
        self.qcbGameList.move(50, 10)
        self.qcbGameList.resize(165, 30)
        self.qcbGameList.currentIndexChanged.connect(self.gameSelectionChange)

        self.qcbPlatformList = QComboBox(self)
        self.qcbPlatformList.addItems(ModuleConfig.PLATFORM_LIST)
        self.qcbPlatformList.move(50, 55)
        self.qcbPlatformList.resize(165, 30)
        self.qcbPlatformList.currentIndexChanged.connect(self.platformSelectionChange)

        leAccount = QLineEdit(self)
        leAccount.setPlaceholderText("本游戏不支持账号登陆!")
        leAccount.setFocusPolicy(Qt.NoFocus)
        leAccount.move(50, 105)
        leAccount.resize(165, 30)

        lePassword = QLineEdit(self)
        lePassword.setPlaceholderText("本游戏不支持账号登陆!")
        lePassword.setFocusPolicy(Qt.NoFocus)
        lePassword.move(50, 150)
        lePassword.resize(165, 30)

        self.leServerName = QLineEdit(self)
        self.leServerName.setPlaceholderText("请输入您所在的区服!")
        self.leServerName.move(50, 195)
        self.leServerName.resize(165, 30)

        buttonLogin = QPushButton('进入游戏', self)
        buttonLogin.move(10, 240)
        buttonLogin.resize(90, 30)
        buttonLogin.clicked.connect(self.login3rd)

        buttonLogin = QPushButton('退出游戏', self)
        buttonLogin.move(125, 240)
        buttonLogin.resize(90, 30)
        buttonLogin.clicked.connect(self.logout)

        self.textEditLog = QTextEdit(self)
        self.textEditLog.move(10, 280)
        self.textEditLog.resize(205, 350)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.textChanged.connect(self.onChangeTextEditLog)

        buttonLogin = QPushButton('清空日志', self)
        buttonLogin.move(10, 640)
        buttonLogin.resize(205, 30)
        buttonLogin.clicked.connect(self.clearLog)

        ###############这块需要封装成一个类###############
        model = QStandardItemModel(4, 4)
        model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        for row in range(3):
            for column in range(4):
                item = QStandardItem('row %s,column %s'%(row, column))
                model.setItem(row, column, item)
        widgetSearchList = QWidget()
        tableView = QTableView(widgetSearchList)
        tableView.resize(500, 500)
        tableView.setModel(model)
        #widgetSearchList.addWidget(tableView)
        widgetPrivateChat = QWidget()
        widgetUnion = QWidget()
        tabWidget = QTabWidget(self)
        tabWidget.move(250, 10)
        tabWidget.resize(500, 655)
        tabWidget.addTab(widgetSearchList, '搜索列表')
        tabWidget.addTab(widgetPrivateChat, '私聊策略')
        tabWidget.addTab(widgetUnion, '帮派')
        ###############这块需要封装成一个类###############

        self.initDefaultData()

    def onChangeTextEditLog(self):
        textCursor = self.textEditLog.textCursor()
        self.textEditLog.moveCursor(textCursor.End)

    def appendLog(self, content):
        self.textEditLog.insertPlainText(content + '\n')

    def clearLog(self):
        self.textEditLog.clear()

    def initDefaultData(self):
        self.qcbGameList.setCurrentText('梦幻诛仙')
        self.qcbPlatformList.setCurrentText('微信-安卓')
        self.leServerName.setText('微信互通107服')

    def gameSelectionChange(self, i):
        self.appendLog('您选择了 ' + ModuleConfig.GAME_LIST[i] + ' 游戏!')

    def platformSelectionChange(self, i):
        self.appendLog('您选择了 ' + ModuleConfig.PLATFORM_LIST[i] + ' 平台!')

    def getServerSelectionKey(self):
        platform = self.qcbPlatformList.currentText()
        serverSelectionKey = ModuleConfig.PALTFORM_MAP[platform]
        serverSelectionKey += '@|||@' + self.leServerName.text()
        return serverSelectionKey

    def packAuthInfo(self, loginInfo, serverInfo):
        if serverInfo['support_multi_system_plats'] == 'true':
            mAccount = (loginInfo['openid'] +
                        '$' + serverInfo['channel'] +
                        '#' + serverInfo['platform'] +
                        '@' + serverInfo['zoneid'])
        else:
            mAccount = (loginInfo['openid'] +
                        '$' + serverInfo['channel'] +
                        '#' + serverInfo['platform'] +
                        '@' + serverInfo['zoneid'])
        mToken = (loginInfo['accessToken'] +
                    '$' + loginInfo['pf'] +
                    '$' + loginInfo['pfKey'] +
                    '$' + serverInfo['platform'] + '_' + serverInfo['channel'])
        deviceInfo = {
            'gameAppid': ModuleConfig.MHZX_APPID,
            'platid': 1,
            'registerChannelid': 10040714,
            'paramMap': {
                '0': 29537,
                '1': 'Android OS 6.0.1 \/ API-23 (V417IR\/eng.duanlusheng.20210513.115441)',
                '2': 'Netease MuMu',
                '3': 'MOBILE',
                '4': 1440,
                '5': 810,
                '6': 320,
                '7': 'processorCount=2,processorType=Intel x86 SSE3',
                '8': 3953,
                '9': 'MuMu GL (Intel Inc. Intel(R) Iris(TM) Plus Graphics OpenGL Engine OpenGL 4.1 core)',
                '10': 'OpenGL ES 2.0 (MuMu GL, Powered by ANGLE 2.1.0.23333333)',
                '11': 'c74ea5ac9b46cfb9cb063c136bac8ed2',
                '12': 0
            },
            'telecomOper': 0,
            'fakePlatform': 0,
            'channelid': '10040714'
        }
        return {
            'mAccount': mAccount,
            'mToken': mToken,
            'loginType': 3,
            'deviceInfo': json.dumps(deviceInfo)
        }
    
    def loginGame(self, loginInfo):
        self.appendLog('获得登陆信息!')
        serverName = ModuleConfig.MHZX_SERVER_NAME
        serverPort = ModuleConfig.MHZX_SERVER_PORT
        gclientObj = ModuleGClient.GClient()
        gclientObj.notifyOutLog.connect(self.appendLog)
        serverMap = gclientObj.getServerMap(serverName, serverPort)
        if not serverMap:
            return False
        try:
            serverSelectionKey = self.getServerSelectionKey()
            serverInfo = serverMap[serverSelectionKey]
        except Exception:
            return False
        self.appendLog('获得服务器信息!')
        serverName = serverInfo['address']
        serverPort = int(serverInfo['portList'][0])
        authInfo = self.packAuthInfo(loginInfo, serverInfo)
        self.appendLog('打包验证信息!')
        self.sclientObj = ModuleSClient.SClient(authInfo)
        self.sclientObj.notifyOutLog.connect(self.appendLog)
        self.sclientObj.connectToGameServer(serverName, serverPort)

    def login3rd(self):
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
        self.appendLog('登陆游戏:' + self.qcbGameList.currentText())
        wechatObj = ModuleWechat.Wechat(ModuleConfig.MHZX_APPID, ModuleConfig.MHZX_MSDK_KEY, headerInfo)
        qrcodeInfo = wechatObj.getQrcodeInfo()
        if not qrcodeInfo:
            return False
        self.qrcodeObj = ModuleQrcode.Qrcode(qrcodeInfo, wechatObj)
        self.qrcodeObj.notifyOutLog.connect(self.appendLog)
        self.qrcodeObj.notifyOut.connect(self.loginGame)
        self.qrcodeObj.showQrcode()


    def logout(self):
        self.appendLog('游戏退出!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())