from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QDialog
)
import moduleWechat as ModuleWechat

class Qrcode(QDialog):
    notifyOut = pyqtSignal(dict)
    notifyOutLog = pyqtSignal(str)

    def __init__(self, qrcodeInfo, wechatObj):
        super(Qrcode, self).__init__()

        qrcodeBinary = qrcodeInfo['qrcodebinary']
        qrcodeDetail = qrcodeInfo['qrcodedetail']

        self._wechatObj = wechatObj

        self.setWindowTitle("扫码登陆")
        self.resize(470, 500)
        self.setWindowModality(Qt.ApplicationModal)

        imageQrcode = QPixmap()
        imageQrcode.loadFromData(qrcodeBinary)

        labelQrcode = QLabel(self)
        labelQrcode.setPixmap(imageQrcode)
        labelQrcode.move(0, 0)

        self.labelDetail = QLabel(self)
        self.labelDetail.setText(qrcodeDetail)
        self.labelDetail.setStyleSheet("""
            font-size: 18px;
            background-color: #660BAB;
        """)
        self.labelDetail.move(0, 470)

    def showQrcode(self):
        self.show()
        self._wechatObj.notifyOut.connect(self.notifyOutCb)
        self._wechatObj.startCheckingQrcodeStatus()

    def closeEvent(self, event):
        event.accept()
        self.notifyOutLog.emit('您放弃了扫描验证!')
        self._wechatObj.stopCheckingQrcodeStatus()

    def notifyOutCb(self, single):
        if single == 1:
            self.notifyOutLog.emit('等待扫描，使用微信扫一扫登陆游戏!')
            self.labelDetail.setText('等待扫描，使用微信扫一扫登陆游戏!')
            self.labelDetail.setStyleSheet("""
                font-size: 18px;
                background-color: #45272C;
            """)
        if single == 2:
            self.notifyOutLog.emit('扫描成功，请在手机上确认登陆!')
            self.labelDetail.setText('扫描成功，请在手机上确认登陆!')
            self.labelDetail.setStyleSheet("""
                font-size: 18px;
                background-color: #007500;
            """)
        if single == 11:
            self.accept()
            self.notifyOutLog.emit('长时间未确认，验证失败!')

        if single == 12:
            self.accept()
            self.notifyOutLog.emit('第三方验证成功!')
            loginInfo = self._wechatObj.getLoginInfo()
            self.notifyOut.emit(loginInfo)