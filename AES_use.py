# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

#用aes加密，再用base64  encode
def aes_encrypt(data, key): 
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    encrypted = cipher.encrypt(pad(data))  #aes加密
    result = base64.b64encode(encrypted)  #base64 encode
    return result

#把加密的数据，用base64  decode，再用aes解密
def aes_decrypt(data, key):
    unpad = lambda s : s[0:-ord(s[-1])]
    cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    result2 = base64.b64decode(data)
    decrypted = unpad(cipher.decrypt(result2))
    return  decrypted

# key = '12345678901234561234567890123456' #此处16|24|32个字符
# data = "test"
# print aes_encrypt(data, key)
# print aes_decrypt(aes_encrypt(data, key), key)

