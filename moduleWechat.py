from PyQt5.QtCore import QThread, pyqtSignal
import time, json, base64, hashlib, ssl
from urllib import request
from urllib import parse
ssl._create_default_https_context = ssl._create_unverified_context

class Wechat(QThread):
    notifyOut = pyqtSignal(int)

    def __init__(self, appid, msdkKey, headerInfo):
        super(Wechat, self).__init__()

        self._appid = appid
        self._msdkKey = msdkKey
        self._checkRuning = True
        self._loginInfo = {}
        self._headerInfo = headerInfo

    def getLoginInfo(self):
        return self._loginInfo

    def reqWxscanLogin(self):
        timestamp = str(round(time.time() * 1000))
        signature = hashlib.md5(str.encode(self._msdkKey + timestamp)).hexdigest()
        url = 'http://msdk.qq.com/auth/wxscan_login'
        url = url + '?timestamp=' + timestamp
        url = url + '&appid=' + self._appid
        url = url + '&sig=' + signature
        url = url + '&opua=' + 'AndroidSDK_21_klte_5.0'
        url = url + '&openid='
        url = url + '&encode=' + str(2)
        paramData = {
            'appid': self._appid
        }
        reqData = request.Request(url, data = json.dumps(paramData).encode('utf-8'))
        resData = request.urlopen(reqData).read().decode('utf-8')
        resDict = json.loads(resData)
        return {
            'ret': resDict['ret'],
            'msg': resDict['msg'],
            'random': resDict['random'],
            'sig': resDict['sig'],
            'timestamp': resDict['timestamp']
        }

    def getQrcodeInfo(self):
        resInfo = self.reqWxscanLogin()
        if resInfo['ret'] != 0:
            return False
        url = 'https://open.weixin.qq.com/connect/sdk/qrconnect'
        url = url + '?appid=' + self._appid
        url = url + '&noncestr=' + resInfo['random']
        url = url + '&timestamp=' + resInfo['timestamp']
        url = url + '&scope=' + 'snsapi_login,snsapi_userinfo,snsapi_friend,snsapi_message'
        url = url + '&signature=' + resInfo['sig']
        resp = request.urlopen(url)
        dataText = resp.read()
        dictData = json.loads(dataText)

        errcode = dictData['errcode']
        errmsg = dictData['errcode']
        if errcode != 0:
            return False
        self._uuid = dictData['uuid']
        appname = dictData['appname']
        qrcodedetail = "[" + "errcode:" + str(errcode) + "|" + "uuid:" + self._uuid + "|" + "appname:" + appname + "]"

        qrcodeInfo = dictData['qrcode']
        qrcodebase64 = qrcodeInfo['qrcodebase64']
        qrcodebinary = base64.b64decode(qrcodebase64)

        return {'qrcodebinary': qrcodebinary,
                'qrcodedetail': qrcodedetail}

    def run(self):
        origin_url = 'https://long.open.weixin.qq.com/connect/l/qrconnect?f=json' + '&uuid=' + self._uuid
        url = origin_url
        while self._checkRuning:
            resp = request.urlopen(url)
            dataText = resp.read()
            dictData = json.loads(dataText)
            wxErrcode = dictData['wx_errcode']
            wxCode = dictData['wx_code']
            if wxErrcode == 408 and self._checkRuning:
                self.notifyOut.emit(1)
            if wxErrcode == 404 and self._checkRuning:
                self.notifyOut.emit(2)
            if wxErrcode == 402:
                self.notifyOut.emit(11)
                break
            if wxErrcode == 405:
                self._loginInfo = self.wxFirstLogin(wxCode)
                self.notifyOut.emit(12)
                break
            url = origin_url + '&last=' + str(wxErrcode)

    def startCheckingQrcodeStatus(self):
        self.start()

    def stopCheckingQrcodeStatus(self):
        self._checkRuning = False

    def wxFirstLogin(self, wxCode):
        timestamp = str(round(time.time() * 1000))
        signature = hashlib.md5(str.encode(self._msdkKey + timestamp)).hexdigest()
        url = 'http://msdk.qq.com/auth/wxfirst_login/'
        url = url + '?timestamp=' + timestamp
        url = url + '&appid=' + self._appid
        url = url + '&sig=' + signature
        url = url + '&opua=' + 'AndroidSDK_21_klte_5.0'
        url = url + '&openid='
        url = url + '&encode=' + str(2)
        url = url + '&version=' + '2.14.5a'
        paramData = {
            'appid': self._appid,
            'channel': self._headerInfo['channel'],
            'offerid': self._headerInfo['offerid'],
            'platform': self._headerInfo['platform'],
            'os': self._headerInfo['os'],
            'grantType': self._headerInfo['grantType'],
            'code': wxCode,
            'grayType': self._headerInfo['grayType'],
            'localIP': self._headerInfo['localIP'],
            'deviceInfo': self._headerInfo['deviceInfo']
        }
        reqData = request.Request(url, data = json.dumps(paramData).encode('utf-8'))
        return json.loads(request.urlopen(reqData).read().decode('utf-8'))
