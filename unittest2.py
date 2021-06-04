from urllib import request
from urllib import parse
import time, hashlib, json
import moduleConfig

def wxFirstLogin(appid, msdkKey, wxCode):
    timestamp = str(round(time.time() * 1000))
    signature = hashlib.md5(str.encode(msdkKey + timestamp)).hexdigest()
    url = 'http://msdk.qq.com/auth/wxfirst_login/'
    url = url + '?timestamp=' + timestamp
    url = url + '&appid=' + appid
    url = url + '&sig=' + signature
    url = url + '&opua=' + 'AndroidSDK_21_klte_5.0'
    url = url + '&openid='
    url = url + '&encode=' + str(2)
    url = url + '&version=' + '2.14.5a'
    paramData = {
        'appid': appid,
        'channel': moduleConfig.MHZX_CHANNEL,
        'offerid': moduleConfig.MHZX_OFFERID,
        'platform': moduleConfig.MHZX_PLATFORM,
        'os': moduleConfig.MHZX_OS,
        'grantType': moduleConfig.MHZX_GRANT_TYPE,
        'code': wxCode,
        'grayType': moduleConfig.MHZX_GRAY_TEST,
        'localIP': moduleConfig.MHZX_LOCAL_IP,
        'deviceInfo': moduleConfig.MHZX_DEVICE_INFO
    }
    reqData = request.Request(url, data = json.dumps(paramData).encode('utf-8'))
    resData = request.urlopen(reqData).read().decode('utf-8')
    resDict = json.loads(resData)
    print(resDict)
    #return {
    #    'ret': resDict['ret'],
    #    'msg': resDict['msg'],
    #    'random': resDict['random'],
    #    'sig': resDict['sig'],
    #    'timestamp': resDict['timestamp']
    #}

wxFirstLogin(moduleConfig.MHZX_APPID, moduleConfig.MHZX_MSDK_KEY, 'wx_code')