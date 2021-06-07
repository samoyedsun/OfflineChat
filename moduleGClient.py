from PyQt5.QtCore import QThread, pyqtSignal
import socket, time, zlib
from xml.dom.minidom import parseString

class GClient(QThread):
    notifyOutLog = pyqtSignal(str)

    def __init__(self):
        super(GClient, self).__init__()
        
        self._socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self._serverMap = {}
        self._running = True
        self._RECV_CATCH_SIZE = 65535

    def sendData(self):
        pass
        # s.send(b'*3\r\n$3\r\nSET\r\n$10\r\nprobeRedis\r\n$10\r\nhelloRedis\r\n')
        
    def getWord(self, data, offset):
        return (((data[offset] & 255) << 8) | (data[offset + 1] & 255)) & 4294934527 # 这里为什么是4294934527, 还没搞清楚

    def getDword(self, data, offset):
        return (((data[offset] & 255) << 24) | ((data[offset + 1] & 255) << 16) | ((data[offset + 2] & 255) << 8) | (data[offset + 3] & 255)) & 1073741823 # 这里又为什么是1073741823

    def getBody(self, data, offset, msgBodyLength):
        msgBody = bytes('', 'utf-8')
        for i in range(msgBodyLength):
            msgBody += data[offset + i].to_bytes(1, 'big')
        return msgBody
        
    def unpackMsgBody7101(self, data):
        def parseField1(field):
            fieldUnziped = zlib.decompress(field)
            fieldXmlDomTree = parseString(fieldUnziped)
            serverGroupList = fieldXmlDomTree.firstChild
            serverGroupList = serverGroupList.getElementsByTagName('servergroup')
            serverMap = {}
            for serverGroup in serverGroupList:
                channel = serverGroup.getAttribute('auth')
                platformList = serverGroup.getAttribute('os').split(',')
                serverList = serverGroup.getElementsByTagName('server')
                for server in serverList:
                    hidden = server.getAttribute('hidden')
                    if hidden == 'true':
                        continue
                    name = server.getAttribute('name')
                    address = server.getAttribute('address')
                    portList = server.getAttribute('port').split(',')
                    support_multi_system_plats = server.getAttribute('support_multi_system_plats')
                    zoneid = server.getAttribute('zoneid')
                    for platform in platformList:
                        serverKey = channel + '@|||@' + platform + '@|||@' + name
                        serverMap[serverKey] = {
                            'channel': channel,
                            'platformList': platformList,
                            'platform': platform,
                            'name': name,
                            'address': address,
                            'portList': portList,
                            'support_multi_system_plats': support_multi_system_plats,
                            'zoneid': zoneid
                        }
            return serverMap
        def parseField2(field):
            fieldUnziped = zlib.decompress(feild)
            fieldXmlDomTree = parseString(fieldUnziped)
            updateInfo = fieldXmlDomTree.toxml()
            # 没大用就不继续解析了
            return updateInfo
        def parseField3(field):
            fieldUnziped = zlib.decompress(field)
            versionList = fieldUnziped.decode()
            # 没大用就不继续解析了
            return versionList
        
        offset = 0
        
        fieldBodyLength = self.getWord(data, offset)
        offset += 2
        field1Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        fieldBodyLength = self.getWord(data, offset)
        offset += 2
        field2Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        fieldBodyLength = self.getWord(data, offset)
        offset += 2
        field3Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        # 数据含义暂不确定
        serverListLength = self.getDword(data, offset)
        offset += 4

        # 数据含义暂不确定
        versionLength = self.getDword(data, offset)
        offset += 4

        # 数据含义暂不确定
        versionListLength = self.getDword(data, offset)
        offset += 4

        serverMap = parseField1(field1Body)
        return serverMap

    def processData(self, data):
        totalLength = len(data)
        self.notifyOutLog.emit('接收到 数据大小:' + str(totalLength))
        offset = 0
        protoId = self.getWord(data, offset)
        offset += 2
        self.notifyOutLog.emit('接收到 协议ID:' + str(protoId))
        msgBodyLength = self.getDword(data, offset)
        offset += 4
        self.notifyOutLog.emit('接收到 消息体长度:' + str(msgBodyLength))
        if protoId == 7101:
            msgBody = self.getBody(data, offset, msgBodyLength)
            serverMap = self.unpackMsgBody7101(msgBody)
            self._serverMap = serverMap
            self._running = False

    def run(self):
        while self._running:
            time.sleep(1)
            data = self._socketObj.recv(self._RECV_CATCH_SIZE)
            if len(data) == 0:
                continue
            self.processData(data)
        self._socketObj.close()

    def getServerMap(self, serverName, serverPort):
        self.notifyOutLog.emit('连接到网关服:' + serverName + ':' + str(serverPort))
        self._socketObj.connect((serverName, serverPort))
        self.start()
        self.wait()
        return self._serverMap