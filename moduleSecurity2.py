import hashlib, random

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

class Decompress:
    def __init__(self):
        self._history = [0] * 8192

        self._histptr = 0
        self._l = 0
        self._adjust_l = 0
        self._blen = 0
        self._blen_totol = 0
        self._rptr = 0
        self._adjust_rptr = 0
    
    def passbits(self, n):
        self._l += n
        self._blen += n
        if self._blen < self._blen_totol:
            return True
        self._l = self._adjust_l
        self._rptr = self._adjust_rptr
        return False

    def fetch(self):
        self._rptr += self._l >> 3
        self._l &= 7

        tmpData = ((self._lbuf[self._rptr + 3] << 24) |
                    (self._lbuf[self._rptr + 2] << 16) |
                    (self._lbuf[self._rptr + 1] << 8) |
                    self._lbuf[self._rptr])

        tmpData = ((tmpData & 255) << 24 |
                (tmpData >> 8 & 255) << 16 |
                (tmpData >> 16 & 255) << 8 |
                (tmpData >> 24 & 255)) << self._l
        return tmpData & 4294967295

    def reserve(self, l, size):
        for i in range(size):
            l.append(0)

    def update(self, data):
        legacy_in = bytesToList(data)
        self._blen_totol = len(data) * 8 - self._l
        self.reserve(legacy_in, 3)
        self._lbuf = legacy_in
        self._rptr = 0
        self._blen = 7
        data = bytes('', 'utf-8')
        num = self._histptr
        while self._blen_totol > self._blen:
            self._adjust_l = self._l
            self._adjust_rptr = self._rptr
            num2 = self.fetch()
            if num2 < 2147483648:
                if not self.passbits(8):
                    break
                array = self._history
                num3 = self._histptr
                self._histptr = num3 + 1
                array[num3] = (num2 >> 24) & 255
            elif num2 < 3221225472:
                if not self.passbits(9):
                    break
                array2 = self._history
                num3 = self._histptr
                self._histptr = num3 + 1
                array2[num3] = (num2 >> 23 | 128) & 255
            else:
                num4 = 0
                if num2 > 4026531840:
                    if not self.passbits(10):
                        break
                    num4 = (num2 >> 22 & 63)
                    if num4 == 0:
                        num5 = 8 - (self._l & 7)
                        if num5 >= 8 or self.passbits(num5):
                            amount = self._histptr - num
                            for i in range(num, amount):
                                data += self._history[i].to_bytes(1, 'big')
                            if self._histptr == 8192:
                                self._histptr = 0
                            num = self._histptr
                            continue
                        break
                elif num2 >= 3758096384:
                    if not self.passbits(12):
                        break
                    num4 = (num2 >> 20 & 255) + 64
                elif num2 >= 3221225472:
                    if not self.passbits(16):
                        break
                    num4 = (num2 >> 16 & 8191) + 320
                num2 = self.fetch()
                num6 = 0
                if num2 < 2147483648:
                    if not self.passbits(1):
                        break
                    num6 = 3
                elif num2 < 3221225472:
                    if not self.passbits(4):
                        break
                    num6 = (4 | (num2 >> 28 & 3))
                elif num2 < 3758096384:
                    if not self.passbits(6):
                        break
                    num6 = (8 | (num2 >> 26 & 7))
                elif num2 < 4026531840:
                    if not self.passbits(8):
                        break
                    num6 = (16 | (num2 >> 24 & 15))
                elif num2 < 4160749568:
                    if not self.passbits(10):
                        break
                    num6 = (32 | (num2 >> 22 & 31))
                elif num2 < 4227858432:
                    if not self.passbits(12):
                        break
                    num6 = (64 | (num2 >> 20 & 63))
                elif num2 < 4261412864:
                    if not self.passbits(14):
                        break
                    num6 = (128 | (num2 >> 18 & 127))
                elif num2 < 4278190080:
                    if not self.passbits(16):
                        break
                    num6 = (256 | (num2 >> 16 & 255))
                elif num2 < 4286578688:
                    if not self.passbits(18):
                        break
                    num6 = (512 | (num2 >> 14 & 511))
                elif num2 < 4290772992:
                    if not self.passbits(20):
                        break
                    num6 = (1024 | (num2 >> 12 & 1023))
                elif num2 < 4292870144:
                    if not self.passbits(22):
                        break
                    num6 = (2048 | (num2 >> 10 & 2047))
                else:
                    if num2 >= 4293918720:
                        self._l = self._adjust_l
                        self._rptr = self._adjust_rptr
                        break
                    if not self.passbits(24):
                        break
                    num6 = (4096 | (num2 >> 8 & 4095))
                if self._histptr < num4 or self._histptr + num6 > 8293:
                    break
                self.lameCopy(self._history, self._histptr, self._histptr - num4, num6)
                self._histptr += num6
        amount = self._histptr - num
        for i in range(num, amount):
            data += self._history[i].to_bytes(1, 'big')
        return data

    def lameCopy(self, arr, dst, src, length):
        if dst - src > 3:
            while length > 3:
                b = arr[src]
                src += 1
                b2 = arr[src]
                src += 1
                b3 = arr[src]
                src += 1
                b4 = arr[src]
                src += 1
                arr[dst] = b
                dst += 1
                arr[dst] = b2
                dst += 1
                arr[dst] = b3
                dst += 1
                arr[dst] = b4
                dst += 1
                length -= 4
        while length > 0:
            arr[dst] = arr[src]
            dst += 1
            src += 1
            length -= 1


class ARCFourSecurity:
    def __init__(self, key):
        self._perm = self.getPerm(key)
        self._keyIndex1 = 0
        self._KeyIndex2 = 0

    def getPerm(self, key):
        keyLength = len(key)
        perm = []
        for i in range(256):
            perm.append(i)
        b1 = 0
        for i in range(256):
            b1 += perm[i]
            b1 += key[i % keyLength]
            b2 = perm[i]
            perm[i] = perm[b1 & 255]
            perm[b1 & 255] = b2
        return perm

    def update(self, data):
        dataList = bytesToList(data)
        for i in range(len(dataList)):
            self._keyIndex1 += 1
            self._KeyIndex2 += self._perm[self._keyIndex1 & 255]
            b1 = self._perm[self._keyIndex1 & 255]
            self._perm[self._keyIndex1 & 255] = self._perm[self._KeyIndex2 & 255]
            self._perm[self._KeyIndex2 & 255] = b1
            b2 = self._perm[self._keyIndex1 & 255] + self._perm[self._KeyIndex2 & 255]
            dataList[i] = dataList[i] ^ self._perm[b2 & 255]
        return listToBytes(dataList)

    def decrypt(self, data):
        pass

class MhzxSecurity:
    def __init__(self, mAccount, mToken, serverKey):
        self._serverKey = serverKey
        self._clientKey = self.generateClientKey(serverKey)
        password = hashlib.md5(str.encode(mAccount + mToken)).digest()

        self._sendKey = self.generateKey(password, mAccount.encode('utf-8'), self._serverKey)
        self._sendCipher = ARCFourSecurity(self._sendKey)

        self._recvKey = self.generateKey(password, mAccount.encode('utf-8'), self._clientKey)
        self._recvCipher = ARCFourSecurity(self._recvKey)

        #self._decompress = Decompress()
        
    def generateClientKey(self, serverKey):
        clientKeyLength = len(serverKey)
        clientKey = bytes('', 'utf-8')
        for i in range(clientKeyLength):
            randNum = random.randint(0, 255)
            clientKey += randNum.to_bytes(1, 'big')
        return clientKey

    def getClientKey(self):
        return self._clientKey
        
    def generateKey(self, password, nonce1, nonce2):
        amount = len(password)
        md5hash = []
        kopad = []
        for i in range(amount):
            md5hash.append(password[i] ^ 54)
            kopad.append(password[i] ^ 92)
        for i in range(amount, 64):
            md5hash.append(54)
            kopad.append(92)
        for i in range(len(nonce1)):
            md5hash.append(nonce1[i])
        for i in range(len(nonce2)):
            md5hash.append(nonce2[i])
        
        md5hash = listToBytes(md5hash)
        realMd5hash = hashlib.md5(md5hash).digest()
        kopad = listToBytes(kopad)
        return hashlib.md5(kopad + realMd5hash).digest()
    
    def encryption(self, data):
        return self._sendCipher.update(data)

    def decryption(self, data):
        oin = self._recvCipher.update(data)
        self._decompress = Decompress()
        return self._decompress.update(oin)