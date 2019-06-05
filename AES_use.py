# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

# pkcs5
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]


# pkcs5
def padding(text):
    text_length = len(text)
    amount_to_pad = AES.block_size - (text_length % AES.block_size)
    if amount_to_pad == 0:
        amount_to_pad = AES.block_size
    pad = chr(amount_to_pad)
    return text + pad * amount_to_pad


# 加密函数
def encrypt(text, key):
    # key = '9999999999999999'
    mode = AES.MODE_CBC
    iv = b'0000000000000000'
    text = pad(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text, key):
    # key = '9999999999999999'
    iv = b'0000000000000000'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return unpad(plain_text)
    # return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    # key = '9999999999999999' 16 | 24 | 32 个字符
    key = 'c24f3213ecd0b4532810d2162d1e3daf4c97335552f911835bd1e48ba3ad116d'
    key = bytes(key.decode('hex'))
    # print str(key)
    data = "userKey"
    # print len(key.decode('hex'))
    e = encrypt(data, key)
    # e = "7d8b9fd45d52d842f9cecb4c087e6d22".decode('hex')  # 加密
    d = decrypt(e, key)  # 解密
    print "加密:", e
    print "解密:", d 

    # e0a42b6596f180d25b2e624b062ba6