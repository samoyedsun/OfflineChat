import hashlib, random, hmac
from Crypto.Cipher import ARC4

class MhzxSecurity:
    def __init__(self, mAccount, mToken, serverKey):
        # 1: MD5生成password
        password = self.getPassword(mAccount, mToken)
        # 2: HMAC_MD5Hash生成sendKey
        #self._sendKey = self.getSendKeyByHmacMd5Hash(password, mAccount, serverKey)
        self._sendKey = self.getSendKeyHmacMd5(password, mAccount, serverKey)
        # 3: 创建ARC4对象
        self._cipher = ARC4.new(self._sendKey)
        # 3: ARC4算法生成sendPerm
        #self._sendPerm = self.getSendPerm(self._sendKey)
        #self._sendKeyIndex1 = 0
        #self._sendKeyIndex2 = 0

    def getSendKey(self):
        return self._sendKey
        
    def getPassword(self, mAccount, mToken):
        #md = hashlib.md5()
        #md.update(mAccount.encode('utf-8'))
        #md.update(mToken.encode('utf-8'))
        return hashlib.md5(str.encode(mAccount + mToken)).hexdigest()
        
    def getSendKeyHmacMd5(self, password, mAccount, serverKey):
        md = hmac.new(password.encode('utf-8'), digestmod = hashlib.md5)
        md.update(mAccount.encode('utf-8'))
        md.update(serverKey)
        return md.hexdigest()
        #print(md.digest())

    def getSendKeyByHmacMd5Hash(self, password, mAccount, serverKey):
        amount = len(password)
        md5hash = []
        kopad = []
        for i in range(amount):
            cn = ord(password[i])
            md5hash.append(cn ^ 54)
            kopad.append(cn ^ 92)
        for i in range(amount, 64):
            md5hash.append(54)
            kopad.append(92)
        for i in range(len(mAccount)):
            cn = ord(mAccount[i])
            md5hash.append(cn)
        for i in range(len(serverKey)):
            md5hash.append(serverKey[i])
        
        md5hash = self.listToBytes(md5hash)
        md5hash = hashlib.md5(md5hash).hexdigest()
        md5hashBytes = bytes('', 'utf-8')
        for i in range(len(md5hash)):
            cn = ord(md5hash[i])
            md5hashBytes += cn.to_bytes(1, 'big')
        kopad = self.listToBytes(kopad)
        sendKey = hashlib.md5(kopad + md5hashBytes).hexdigest()
        return sendKey

    def getSendPerm(self, sendKey):
        sendKeyLength = len(sendKey)
        perm = []
        for i in range(256):
            perm.append(i)
        b1 = 0
        for i in range(256):
            b1 += perm[i]
            b1 += ord(sendKey[i % sendKeyLength])
            b2 = perm[i]
            perm[i] = perm[b1 & 255]
            perm[b1 & 255] = b2
        return perm

    def getClientKey(self, serverKey):
        clientKeyLength = len(serverKey)
        clientKeyList = []
        for i in range(clientKeyLength):
            clientKeyList.append(random.randint(0, 255))
        return self.listToBytes(clientKeyList)
        
    def encryption(self, data):
        return self._cipher.encrypt(data)
        '''
        dataList = self.bytesToList(data)
        for i in range(len(dataList)):
            self._sendKeyIndex1 += 1
            self._sendKeyIndex2 += self._sendPerm[self._sendKeyIndex1 & 255]
            b1 = self._sendPerm[self._sendKeyIndex1 & 255]
            self._sendPerm[self._sendKeyIndex1 & 255] = self._sendPerm[self._sendKeyIndex2 & 255]
            self._sendPerm[self._sendKeyIndex2 & 255] = b1
            b2 = self._sendPerm[self._sendKeyIndex1 & 255] + self._sendPerm[self._sendKeyIndex2 & 255]
            dataList[i] = dataList[i] ^ self._sendPerm[b2 & 255]
        return self.listToBytes(dataList)
        '''

    def listToBytes(self, l):
        b = bytes('', 'utf-8')
        for v in l:
            b += v.to_bytes(1, 'big')
        return b
    
    def bytesToList(self, b):
        l = []
        for v in b:
            l.append(v)
        return l