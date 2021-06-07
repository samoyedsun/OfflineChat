import socket, time, threading, zlib
from xml.dom.minidom import parseString

import moduleConfig

class SClient():
    def __init__(self, serverName, serverPort):
        self._serverName = serverName
        self._serverPort = serverPort
        self._socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self._running = True
        self._RECV_CATCH_SIZE = 65535

    def sendData(self):
        pass
        # s.send(b'*3\r\n$3\r\nSET\r\n$10\r\nprobeRedis\r\n$10\r\nhelloRedis\r\n')

    def recvLoop(self):
        while self._running:
            time.sleep(1)
            data = self._socketObj.recv(self._RECV_CATCH_SIZE)
            if len(data) == 0:
                continue
            msg = self.parseData(data)
            self.processMsg(msg)
        self.close()

    def getWord(self, data, offset):
        return (((data[offset] & 255) << 8) | (data[offset + 1] & 255)) & 4294934527 # 这里为什么是4294934527, 还没搞清楚

    def getDword(self, data, offset):
        return (((data[offset] & 255) << 24) | ((data[offset + 1] & 255) << 16) | ((data[offset + 2] & 255) << 8) | (data[offset + 3] & 255)) & 1073741823 # 这里又为什么是1073741823

    def getBody(self, data, offset, msgBodyLength):
        msgBody = bytes('', 'utf-8')
        for i in range(msgBodyLength):
            msgBody += data[offset + i].to_bytes(1, 'big')
        return msgBody
        
    def parseMsgBody7101(self, data):
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
        print('字段一长度:', fieldBodyLength)
        field1Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        fieldBodyLength = self.getWord(data, offset)
        offset += 2
        print('字段二长度:', fieldBodyLength)
        field2Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        fieldBodyLength = self.getWord(data, offset)
        offset += 2
        print('字段三长度:', fieldBodyLength)
        field3Body = self.getBody(data, offset, fieldBodyLength)
        offset += fieldBodyLength

        # 数据含义暂不确定
        serverListLength = self.getDword(data, offset)
        offset += 4
        print('字段四:', serverListLength)

        # 数据含义暂不确定
        versionLength = self.getDword(data, offset)
        offset += 4
        print('字段五:', versionLength)

        # 数据含义暂不确定
        versionListLength = self.getDword(data, offset)
        offset += 4
        print('字段六:', versionListLength)

        serverMap = parseField1(field1Body)
        return serverMap

    def parseData(self, data):
        totalLength = len(data)
        print("总长度:", totalLength)
        offset = 0
        protoId = self.getWord(data, offset)
        offset += 2
        print('协议ID:', protoId)
        msgBodyLength = self.getDword(data, offset)
        offset += 4
        print('消息体长度:', msgBodyLength)
        if protoId == 7101:
            msgBody = self.getBody(data, offset, msgBodyLength)
            serverMap = self.parseMsgBody7101(msgBody)
            return {
                'protoId': protoId,
                'serverMap': serverMap
            }

    def processMsg(self, msg):
        print(msg)
        self._running = False

    def start(self):
        self._socketObj.connect((self._serverName, self._serverPort))
        threadObj = threading.Thread(target = self.recvLoop)
        # threadObj.setDaemon(True) # 意思是整个进程退出的时候，这个线程不管有没有处理完都要跟着退出
        threadObj.start()
    
    def close(self):
        self._socketObj.close()

sclientObj = SClient(moduleConfig.MHZX_SERVER_NAME, moduleConfig.MHZX_SERVER_PORT)
sclientObj.start()