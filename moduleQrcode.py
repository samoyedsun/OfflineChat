from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QDialog
)
import moduleWechat as ModuleWechat

class Qrcode(QDialog):
    def __init__(self, qrcodeBinary, qrcodeDetail):
        super(Qrcode, self).__init__()

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

    def showQrcode(self, wechatObj):
        wechatObj.notifyOut.connect(self.notifyOutCb)
        wechatObj.startCheckingQrcodeStatus()
        self.exec()
        wechatObj.stopCheckingQrcodeStatus()
        return wechatObj.getLoginInfo()

    def notifyOutCb(self, single):
        if single == 1:
            self.labelDetail.setText('等待扫描，使用微信扫一扫登陆游戏!')
            self.labelDetail.setStyleSheet("""
                font-size: 18px;
                background-color: #45272C;
            """)
        if single == 2:
            self.labelDetail.setText('扫描成功，请在手机上确认登陆!')
            self.labelDetail.setStyleSheet("""
                font-size: 18px;
                background-color: #007500;
            """)
        if single == 11:
            self.accept()