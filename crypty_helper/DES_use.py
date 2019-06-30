#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0
from pyDes import des, CBC, PAD_PKCS5
import binascii
import hashlib
 
# 秘钥
# KEY='mHAxsLYz'
def des_encrypt(s,key):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    key = key[0:8]
    secret_key = key
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)
 
 
def des_decrypt(s, key):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    key = key[0:8]
    secret_key = key
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de
