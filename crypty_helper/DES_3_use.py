#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0
from pyDes import triple_des, CBC, PAD_PKCS5
import binascii
import hashlib
 
# 秘钥
# KEY='mHAxsLYz'
def three_des_encrypt(s,key):
    """
    3DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    s = s.encode()
    key = bytes(key)[0:24]
    secret_key = key
    iv = secret_key[0:8]
    k = triple_des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)
 
 
def three_des_decrypt(s, key):
    """
    3DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    s = s.encode()
    key = bytes(key)[0:24]
    secret_key = key
    iv = secret_key[0:8]
    k = triple_des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de
