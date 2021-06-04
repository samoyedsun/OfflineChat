import base64
import json
import hashlib
import urllib.request
import ssl
import sys
from PyQt5 import QtWidgets, QtGui, QtCore


ssl._create_default_https_context = ssl._create_unverified_context

def getQrcodeInfo():
    url = 'https://open.weixin.qq.com/connect/sdk/qrconnect?appid=wx6b8b5b718858a88b&noncestr=prntfmuonm&timestamp=1622185173&scope=snsapi_login,snsapi_userinfo,snsapi_friend,snsapi_message&signature=5d9c9cc40681e71990ad3ebd70d91758dbc00bd7'
    resp = urllib.request.urlopen(url)
    dataText = resp.read()
    dictData = json.loads(dataText)

    errcode = dictData['errcode']
    uuid = dictData['uuid']
    appname = dictData['appname']
    qrcodedetail = "[" + "errcode:" + str(errcode) + "|" + "uuid:" + uuid + "|" + "appname:" + appname + "]"

    qrcodeInfo = dictData['qrcode']
    qrcodebase64 = qrcodeInfo['qrcodebase64']
    qrcodebinary = base64.b64decode(qrcodebase64)

    return {'qrcodebinary':qrcodebinary,
            'qrcodedetail':qrcodedetail}

#定义窗口函数window
def window():
    #我事实上不太明白干嘛要这一句话，只是pyqt窗口的建立都必须调用QApplication方法
    app = QtWidgets.QApplication(sys.argv)

    #新建一个窗口，名字叫做w
    w = QtWidgets.QWidget()
    #定义w的大小
    w.setGeometry(400, 400, 470, 500)
    #给w一个Title
    w.setWindowTitle('扫码登陆')

    #调用QtGui.QPixmap方法，打开一个图片，存放在imge_qrcode变量中
    qrcodeInfo = getQrcodeInfo()
    qrcodebinary = qrcodeInfo['qrcodebinary']
    qrcodedetail = qrcodeInfo['qrcodedetail']
    image_qrcode = QtGui.QPixmap()
    image_qrcode.loadFromData(qrcodebinary)

    #在窗口w中，新建一个lable，名字叫做l1
    l1 = QtWidgets.QLabel(w)
    # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
    l1.setPixmap(image_qrcode)

    #在窗口w中，新建另一个label，名字叫做l2
    l2=QtWidgets.QLabel(w)
    #调用setText命令，在l2中显示刚才的内容
    l2.setText(qrcodedetail)
    print(QtCore.Qt.AlignHCenter)
    l2.setStyleSheet('background-color: rgb(255, 0, 0)')
    l2.setAlignment(QtCore.Qt.AlignHCenter)

    #调整l1和l2的位置
    l1.move(0, 0)
    l2.move(0, 470)
    #显示整个窗口
    w.show()
    #退出整个app
    app.exit(app.exec_())

#调用window这个函数
window()

'''
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        self.setWindowTitle("抓取工具")

        self.resize(400, 300)
        self.status = self.statusBar()
        self.status.showMessage('抓取工具')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWin()
    mainWin.show()

    sys.exit(app.exec_())
'''

'''
import tkinter
window = tkinter.Tk()
im = tkinter.PhotoImage(data="data:image/jpeg;base64," + qrcodebase64)
#tk.Label(root, image=im).pack()
window.mainloop()
print(tkinter.TkVersion)
'''


'''
url = 'http://cloud.gsdk.qq.com:18081/?cmdid=3&appid=1105938573'
resStr = requests.get(url).text
resSrc = base64.b64decode(resStr)
print(resSrc)

charList = []
for char in resSrc:
    charList.insert(0, char)
print(chr(charList[0] + charList[1]))

charList = []
for char in resSrc:
    charList.insert(0, chr(char))
print(charList)

#########################################################
print('#################################################')

url = 'http://android.bugly.qq.com/rqd/async?aid=5407fd2d-3a66-4d43-b24a-e049ac491e0d'
myobj = {}
x = requests.post(url, data = myobj)
print(x.text)

mkey = 'tencentmsdk1105938573'
timestamp = '1622000438'
print(hashlib.md5(str.encode(mkey + timestamp)).hexdigest())

url = 'http://apps.game.qq.com/ams/ame/gac.php?returntype=html'
resStr = requests.get(url).text
resSrc = resStr.encode('utf-8').decode("unicode-escape")
print(resSrc)

url = 'http://182.254.116.117/d?dn=e4a30b77424e17d729ad13c95d360e83407d631405df3425&clientip=1&ttl=1&id=1'
resStr = requests.get(url).text
print(resStr)

appid = 'wx6b8b5b718858a88b'
noncestr = 'gufidvdrpn'
timestamp = '1622181937'
signatureSrc = 'appid=' + appid + '&noncestr=' + noncestr + '&timestamp=' + timestamp
signature = hashlib.sha1(signatureSrc.encode('utf-8')).hexdigest()
print("new:", signature)
print("old:", "142db180411dda11e9ea59f69c24b1206bf750d0")

'''
