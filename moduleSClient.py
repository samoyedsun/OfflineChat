from PyQt5.QtCore import QThread, pyqtSignal
import socket, time, json

class SClient(QThread):
    notifyOutLog = pyqtSignal(str)

    def __init__(self, authInfo):
        super(SClient, self).__init__()

        self._authInfo = authInfo
        self._socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self._serverMap = {}
        self._running = True
        self._RECV_CATCH_SIZE = 65535

    def sendData(self, data):
        return self._socketObj.send(data)
    
    def getByte(self, data, offset):
        return data[offset]

    def getWord(self, data, offset):
        return (((data[offset] & 255) << 8) |
                (data[offset + 1] & 255)) & 4294934527 # 这里为什么是4294934527, 还没搞清楚

    def getDword(self, data, offset):
        return (((data[offset] & 255) << 24) |
                ((data[offset + 1] & 255) << 16) |
                ((data[offset + 2] & 255) << 8) |
                (data[offset + 3] & 255))

    def getDDword(self, data, offset):
        return (((data[offset] & 255) << 56) |
                ((data[offset + 1] & 255) << 48) |
                ((data[offset + 2] & 255) << 40) |
                ((data[offset + 3] & 255) << 32) |
                ((data[offset + 4] & 255) << 24) |
                ((data[offset + 5] & 255) << 16) |
                ((data[offset + 6] & 255) << 8) |
                (data[offset + 7] & 255))

    def getBody(self, data, offset, msgBodyLength):
        msgBody = bytes('', 'utf-8')
        for i in range(msgBodyLength):
            msgBody += data[offset + i].to_bytes(1, 'big')
        return msgBody
        
    def unpackMsgBody101(self, data):
        offset = 0

        nonceLength = self.getByte(data, offset)
        offset += 1
        nonce = self.getBody(data, offset, nonceLength)
        nonce = ''.join([hex(v) for v in nonce])
        offset += nonceLength

        version = self.getDword(data, offset)
        offset += 4

        flags = self.getDword(data, offset)
        offset += 4

        load = self.getByte(data, offset)
        offset += 1

        extraLength = self.getByte(data, offset)
        offset += 1
        extra = {}
        for i in range(extraLength):
            key = self.getDword(data, offset)
            offset += 4
            val = self.getDword(data, offset)
            offset += 4
            extra[str(key)] = val

        extra2Length = self.getByte(data, offset)
        offset += 1
        extra2 = {}
        for i in range(extra2Length):
            key = self.getDword(data, offset)
            offset += 4
            val = self.getDword(data, offset)
            offset += 4
            extra2[str(key)] = val

        return {
            'nonce': nonce,
            'version': version,
            'flags:': flags,
            'load': load,
            'extra': extra,
            'extra2': extra2
        }
    
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
        protoId = 103

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


    def processData(self, data):
        totalLength = len(data)
        self.notifyOutLog.emit('接收到 数据大小:' + str(totalLength))
        offset = 0
        protoId = self.getByte(data, offset)
        offset += 1
        self.notifyOutLog.emit('接收到 协议ID:' + str(protoId))
        msgBodyLength = self.getWord(data, offset)
        offset += 2
        self.notifyOutLog.emit('接收到 消息体长度:' + str(msgBodyLength))
        if protoId == 101:
            self.notifyOutLog.emit('解析并处理协议:' + str(protoId))
            msgBody = self.getBody(data, offset, msgBodyLength)
            msgData = self.unpackMsgBody101(msgBody)
            
            protoId = 103
            msgBody = self.packMsgBody103()
            data = bytes('', 'utf-8')
            data += self.numberToShortBytes(protoId)
            data += self.numberToShortBytes(len(msgBody))
            data += msgBody
            sendDataRet = self.sendData(data)
            self.notifyOutLog.emit('sendDataRet:' + str(sendDataRet))
        if protoId == 106:
            self.notifyOutLog.emit('解析并处理协议:' + str(protoId))

    def run(self):
        while self._running:
            self.notifyOutLog.emit('####一秒有后接收数据####')
            time.sleep(1)
            data = self._socketObj.recv(self._RECV_CATCH_SIZE)
            if len(data) == 0:
                continue
            self.processData(data)
        self._socketObj.close()

    def connectToGameServer(self, serverName, serverPort):
        self.notifyOutLog.emit('连接到游戏服:' + serverName + ':' + str(serverPort))
        self._socketObj.connect((serverName, serverPort))
        self.start()