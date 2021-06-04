from urllib import request
from urllib import parse
import time, json, base64, ssl, hashlib

from config import MHZX_APPID
from config import MHZX_MSDK_KEY

ssl._create_default_https_context = ssl._create_unverified_context

def reqWxscanLogin(appid, msdkKey):
    timestamp = str(round(time.time() * 1000))
    signature = hashlib.md5(str.encode(msdkKey + timestamp)).hexdigest()
    url = 'http://msdk.qq.com/auth/wxscan_login'
    url = url + '?timestamp=' + timestamp
    url = url + '&appid=' + appid
    url = url + '&sig=' + signature
    url = url + '&opua=' + 'AndroidSDK_21_klte_5.0'
    url = url + '&openid='
    url = url + '&encode=' + str(2)
    paramData = {
        'appid': appid
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

def getQrcodeInfo(appid, msdkKey):
    resInfo = reqWxscanLogin(appid, msdkKey)
    if resInfo['ret'] != 0:
        print('reqWxscanLogin接口出错, ret:', resInfo['ret'], ', msg:', resInfo['msg'])
        return False
    url = 'https://open.weixin.qq.com/connect/sdk/qrconnect'
    url = url + '?appid=' + appid
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
        print('getQrcodeInfo接口出错, errcode:', errcode, ', errmsg:', errmsg)
        return False
    uuid = dictData['uuid']
    appname = dictData['appname']
    qrcodedetail = "[" + "errcode:" + str(errcode) + "|" + "uuid:" + uuid + "|" + "appname:" + appname + "]"

    qrcodeInfo = dictData['qrcode']
    qrcodebase64 = qrcodeInfo['qrcodebase64']
    qrcodebinary = base64.b64decode(qrcodebase64)

    return {'uuid': uuid,
            'qrcodebinary': qrcodebinary,
            'qrcodedetail': qrcodedetail}
print(getQrcodeInfo(MHZX_APPID, MHZX_MSDK_KEY))