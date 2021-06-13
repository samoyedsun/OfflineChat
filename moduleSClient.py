from PyQt5.QtCore import QThread, pyqtSignal
import socket, time, json

import moduleSecurity as ModuleSecurity

class SClient(QThread):
    notifyOutLog = pyqtSignal(str)

    def __init__(self, authInfo):
        super(SClient, self).__init__()

        self._authInfo = authInfo
        self._socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self._serverMap = {}
        self._running = True
        self._RECV_CATCH_SIZE = 65535
        self._mhzxSecurityObj = None

    def sendData(self, protoId, msgBody):
        data = bytes('', 'utf-8')
        if protoId <= 128:
            data += self.numberToUByteBytes(protoId)
        else:
            realProtoId = protoId | 3221225472
            data += self.numberToUIntBytes(realProtoId)
        msgBodyLength = len(msgBody)
        if msgBodyLength <= 128:
            data += self.numberToUByteBytes(msgBodyLength)
        else:
            data += self.numberToShortBytes(msgBodyLength)
        data += msgBody
        if self._mhzxSecurityObj:
            data = self._mhzxSecurityObj.encryption(data)
        sendLenth = self._socketObj.send(data)
        self.notifyOutLog.emit('发送数据, 协议:' + str(protoId))
        self.notifyOutLog.emit('发送数据, 长度:' + str(sendLenth))

    def getByte(self, offset, data):
        return offset + 1, data[offset]

    def getWord(self, offset, data):
        return offset + 2, (((data[offset] & 255) << 8) |
                (data[offset + 1] & 255))

    def getDword(self, offset, data):
        return offset + 4, (((data[offset] & 255) << 24) |
                ((data[offset + 1] & 255) << 16) |
                ((data[offset + 2] & 255) << 8) |
                (data[offset + 3] & 255))

    def getDDword(self, offset, data):
        return (((data[offset] & 255) << 56) |
                ((data[offset + 1] & 255) << 48) |
                ((data[offset + 2] & 255) << 40) |
                ((data[offset + 3] & 255) << 32) |
                ((data[offset + 4] & 255) << 24) |
                ((data[offset + 5] & 255) << 16) |
                ((data[offset + 6] & 255) << 8) |
                (data[offset + 7] & 255))
    
    def getBodyLength(self, offset, data):
        header = data[offset] & 128
        if header == 128: # 说明是符号位
            offset, length = self.getWord(offset, data)
            length &= 4294934527 # 这里为什么是4294934527, 还没搞清楚
        if header == 0:
            offset, length = self.getByte(offset, data)
        return offset, length

    def getProtoId(self, offset, data):
        if data[offset] & 192 == 192: # 说明是符号位
            offset, protoId = self.getDword(offset, data)
            protoId &= 1073741823 # 这里为什么是1073741823, 还没搞清楚
        elif data[offset] & 128 == 128:
            offset, protoId = self.getWord(offset, data)
            protoId &= 4294934527 # 这里为什么是4294934527, 还没搞清楚
        else:
            offset, protoId = self.getByte(offset, data)
        return offset, protoId

    def getBody(self, offset, data, bodyLength):
        msgBody = bytes('', 'utf-8')
        for i in range(bodyLength):
            msgBody += data[offset + i].to_bytes(1, 'big')
        return offset + bodyLength, msgBody
        
    def unpackMsgBody101(self, data):
        offset = 0
        offset, bodyLength = self.getByte(offset, data)
        offset, body = self.getBody(offset, data, bodyLength)
        nonce = ''.join([hex(v) for v in body])
        offset, version = self.getDword(offset, data)
        offset, flags = self.getDword(offset, data)
        offset, load = self.getByte(offset, data)
        offset, extraLength = self.getByte(offset, data)
        extra = {}
        for i in range(extraLength):
            offset, key = self.getDword(offset, data)
            offset, val = self.getDword(offset, data)
            extra[str(key)] = val
        offset, extra2Length = self.getByte(offset, data)
        extra2 = {}
        for i in range(extra2Length):
            offset, key = self.getDword(offset, data)
            offset, val = self.getDword(offset, data)
            extra2[str(key)] = val
        return {
            'nonce': nonce,
            'version': version,
            'flags:': flags,
            'load': load,
            'extra': extra,
            'extra2': extra2
        }

    def dumpBytesData(self, data):
        self.notifyOutLog.emit('dumpBytesData:' + '|'.join([hex(v) for v in data]))

    def unpackMsgBody106(self, data):
        offset = 0
        offset, bodyLength = self.getBodyLength(offset, data)
        offset, serverKey = self.getBody(offset, data, bodyLength)
        offset, keyType = self.getDword(offset, data)
        return {
            'serverKey': serverKey,
            'keyType': keyType
        }

    def unpackMsgBody110(self, data):
        offset = 0
        offset, bodyLength = self.getBodyLength(offset, data)
        offset, userId = self.getBody(offset, data, bodyLength)
        offset, localSid = self.getDword(offset, data)
        offset, remainTime = self.getDword(offset, data)
        offset, zoneid = self.getDword(offset, data)
        offset, aid = self.getDword(offset, data)
        offset, algorithm = self.getDword(offset, data)
        offset, bodyLength = self.getBodyLength(offset, data)
        #offset, reconnectToken = self.getBody(offset, data, bodyLength)
        body110 = {
            'userId': userId,
            'localSid': localSid,
            'remainTime': remainTime,
            'zoneid': zoneid,
            'aid': aid,
            'algorithm': algorithm
        }
        return body110
    
    def numberToUByteBytes(self, number):
        return number.to_bytes(1, 'big')

    def numberToShortBytes(self, number):
        byte1 = (number | 32768) >> 8 #这里32768是一个符号位，说明是有符号的
        byte2 = number & 255
        byte1 = byte1.to_bytes(1, 'big')
        byte2 = byte2.to_bytes(1, 'big')
        return byte1 + byte2

    def numberToUIntBytes(self, number):
        byte1 = (number >> 24) & 255
        byte2 = (number >> 16) & 255
        byte3 = (number >> 8) & 255
        byte4 = number & 255
        byte1 = byte1.to_bytes(1, 'big')
        byte2 = byte2.to_bytes(1, 'big')
        byte3 = byte3.to_bytes(1, 'big')
        byte4 = byte4.to_bytes(1, 'big')
        return byte1 + byte2 + byte3 + byte4

    def packMsgBody103(self):
        data = bytes('', 'utf-8')

        mAccount = self._authInfo['mAccount']
        data += self.numberToUByteBytes(len(mAccount))
        data += bytes(mAccount, 'utf-8')

        mToken = self._authInfo['mToken']
        data += self.numberToShortBytes(len(mToken))
        data += bytes(mToken, 'utf-8')
        
        loginType = self._authInfo['loginType']
        data += self.numberToUIntBytes(loginType)

        data += self.numberToUByteBytes(0)

        deviceInfo = self._authInfo['deviceInfo']
        data += self.numberToShortBytes(len(deviceInfo))
        data += bytes(deviceInfo, 'utf-8')

        data += self.numberToUByteBytes(0)
        data += self.numberToUByteBytes(0)
        data += self.numberToUByteBytes(0)
        data += self.numberToUByteBytes(0)

        return data

    def packMsgBody106(self):
        clientKey = self._mhzxSecurityObj.getClientKey()

        data = bytes('', 'utf-8')

        data += self.numberToUByteBytes(len(clientKey))
        data += clientKey

        data += self.numberToUIntBytes(1)

        return data

    def packMsgBody12590082(self):
        data = bytes('', 'utf-8')
        data += self.numberToUIntBytes(0)
        data += self.numberToUIntBytes(0)
        return data

    def processData(self, data):
        self.notifyOutLog.emit('接收到 解密前数据大小:' + str(len(data)))
        if self._mhzxSecurityObj:
            data = self._mhzxSecurityObj.decryption(data)
        totalLength = len(data)
        self.notifyOutLog.emit('接收到 解密后数据大小:' + str(totalLength))
        if totalLength == 0:
            return
        offset = 0
        offset, protoId = self.getProtoId(offset, data)
        self.notifyOutLog.emit('接收到 协议ID:' + str(protoId))
        offset, bodyLength = self.getBodyLength(offset, data)
        self.notifyOutLog.emit('接收到 消息体长度:' + str(bodyLength))
        if protoId == 101:
            offset, msgBody = self.getBody(offset, data, bodyLength)
            msgData = self.unpackMsgBody101(msgBody)
            
            protoId = 103
            msgBody = self.packMsgBody103()
            self.sendData(protoId, msgBody)

        if protoId == 106:
            offset, msgBody = self.getBody(offset, data, bodyLength)
            msgData = self.unpackMsgBody106(msgBody)

            serverKey = msgData['serverKey']
            mAccount = self._authInfo['mAccount']
            mToken = self._authInfo['mToken']
            self._mhzxSecurityObj = ModuleSecurity.MhzxSecurity(mAccount, mToken, serverKey)

            protoId = 106
            msgBody = self.packMsgBody106()
            self.sendData(protoId, msgBody)

        if protoId == 110:
            offset, msgBody = self.getBody(offset, data, bodyLength)
            msgData = self.unpackMsgBody110(msgBody)

            protoId = 12590082
            msgBody = self.packMsgBody12590082()
            self.sendData(protoId, msgBody)

        if protoId == 12590042:
            offset, msgBody = self.getBody(offset, data, bodyLength)
            #msgData = self.unpackMsgBody110(msgBody)

    def run(self):
        while self._running:
            time.sleep(1)
            #self.notifyOutLog.emit('开始读取数据')
            data = self._socketObj.recv(self._RECV_CATCH_SIZE)
            #self.notifyOutLog.emit('结束读取数据:' + str(len(data)))
            if len(data) == 0:
                continue
            self.processData(data)
        self._socketObj.close()

    def connectToGameServer(self, serverName, serverPort):
        self.notifyOutLog.emit('连接到游戏服:' + serverName + ':' + str(serverPort))
        self._socketObj.connect((serverName, serverPort))
        self.start()