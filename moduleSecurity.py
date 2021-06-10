import hashlib, random, hmac
from Crypto.Cipher import ARC4

def listToBytes(l):
    b = bytes('', 'utf-8')
    for v in l:
        b += v.to_bytes(1, 'big')
    return b

def bytesToList(b):
    l = []
    for v in b:
        l.append(v)
    return l

class MhzxSecurity:
    def __init__(self, mAccount, mToken, serverKey):
        self._serverKey = serverKey
        self._clientKey = self.generateClientKey(serverKey)
        password = hashlib.md5(str.encode(mAccount + mToken)).digest()
        
        self._sendKey = self.generateKey(password, mAccount.encode('utf-8'), self._serverKey)
        self._sendCipher = ARC4.new(self._sendKey)

        self._recvKey = self.generateKey(password, mAccount.encode('utf-8'), self._clientKey)
        self._recvCipher = ARC4.new(self._recvKey)

    def generateKey(self, password, nonce1, nonce2):
        md = hmac.new(password, digestmod = hashlib.md5)
        md.update(nonce1)
        md.update(nonce2)
        return md.digest()

    def generateClientKey(self, serverKey):
        clientKeyLength = len(serverKey)
        clientKey = bytes('', 'utf-8')
        for i in range(clientKeyLength):
            randNum = random.randint(0, 255)
            clientKey += randNum.to_bytes(1, 'big')
        return clientKey
        
    def getClientKey(self):
        return self._clientKey

    def encryption(self, data):
        return self._sendCipher.encrypt(data)

    def decryption(self, data):
        return self._recvCipher.decrypt(data)