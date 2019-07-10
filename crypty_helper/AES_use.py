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
def aes_encrypt(text, key):
    key = bytes(key.decode('hex'))[0:16]
    # print len(key)
    # key = '9999999999999999'
    mode = AES.MODE_CBC
    # iv = b'0000000000000000'
    iv = key[0:16]
    # print len(iv)
    text = pad(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def aes_decrypt(text, key):
    key = bytes(key.decode('hex'))[0:16]
    # key = '9999999999999999'
    # iv = b'0000000000000000'
    iv = key[0:16]
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return unpad(plain_text)
    # return bytes.decode(plain_text).rstrip('\0')


# if __name__ == '__main__':
#     # key = '9999999999999999' 16 | 24 | 32 个字符
    # key = 'b0282e1fb6a4cdfc583e44a367b68f635c716db6558e90442388c8bcfab0ca3a'
#     key = bytes(key.decode('hex'))
#     # print str(key)
    # data = "userKey"
#     # print len(key.decode('hex'))
    # e = aes_encrypt(data, key)
#     # e = "e0a42b6596f180d25b2e624b062ba64f"
    # d = aes_decrypt(e, key)  # 解密
    # print "加密:", e
    # print "解密:", d 

    # e0a42b6596f180d25b2e624b062ba64f
