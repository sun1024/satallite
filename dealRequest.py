#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0

import time, random
import json, hashlib, requests
import hmac

from crypty_helper.xor import *
from crypty_helper.AES_use import *
from crypty_helper.DES_use import *
from crypty_helper.DES_3_use import *
from crypty_helper.RSA_sign import *
from gl import *
from models import *

# 认证信息
def authCheck(userData, satalliteData):
    masterKey = "0"
    # 解析用户、卫星的认证字段
    ru = userData['Ru']
    MACu = userData['MACu']
    Tu = userData['Tu']
    PIDu = userData['PIDu']
    Hu = userData['Hu']

    rs = satalliteData['Rs']
    MACs = satalliteData['MACs']
    Ts = satalliteData['Ts']
    PIDs = satalliteData['PIDs']
    Hs = satalliteData['Hs']

    # 验证timestamp
    if is_timeout(Ts):
        raise Exception('timeout')

    # 计算出IDu、IDs
    IDu = xor_decrypt(PIDu, Hu) 
    IDs = xor_decrypt(PIDs, Hs) 
    # print IDu, IDs

    # 查询出IDu, IDs对应的信息
    real_sata_data = getAuthData(IDs)
    real_user_data = getAuthData(IDu)

    # 计算出Rs, Ru
    tmp = getHash(real_sata_data['userKey'] + real_sata_data['preRandom'])
    Rs = xor_decrypt(rs, tmp)
    tmp = getHash(real_user_data['userKey'] + real_user_data['preRandom'])
    Ru = xor_decrypt(ru, tmp)

    # 验证MACs MACu
    real_MACs = getHash(real_sata_data['userId'] + Rs + Ts)
    real_MACu = getHash(real_user_data['userId'] + Ru + Tu)

    if MACu == real_MACu and MACs == real_MACs:
        # 生成masterKey 同时产生sk、mac_key
        masterKey = getHash(real_user_data['userKey'] + real_sata_data['preRandom'] + rs)

        sk = getHash(masterKey + real_sata_data["userKey"])
        MAC_key = getHash(real_sata_data["userKey"] + masterKey + rs)
        keys = {
            "sk": sk,
            "MAC_Key": MAC_key
        }
        add_session(PIDu, keys)
    return masterKey

# 返回认证信息
def retSatallite(masterKey):
    sign = rsa_sign(masterKey).encode('hex')
    return {
        "Code": "0",
        "Signiture": sign,
        "MasterKey": masterKey
    }

# 向卫星返回用户信息
def getUserInfo(data):
    PIDu = data['PIDu']
    Hu = data['Hu']
    Ts = data['Ts']

    # 验证timestamp
    if is_timeout(Ts):
        raise Exception('timeout')

    # 通过PIDu拿到sk、MAC_key
    sk, MAC_key = get_sessions(PIDu)
    # 验证MAC
    MAC = data['MAC']
    msg = "ReqUserInfo" + Ts + PIDu + Hu
    my_MAC = getHmac(MAC_key, msg)
    if MAC == my_MAC:
        # 读取用户信息 返回给卫星
        IDu = xor_decrypt(PIDu, Hu) 
        user_data = getAuthData(IDu)

        AesIDu = encryptData(user_data['userId'], sk)
        AesKIu = encryptData(user_data['userKey'], sk)
        Tncc = str(int(time.time()))
        msg = AesIDu + AesKIu + Tncc
        HMAC = getHmac(MAC_key, msg)

        return {
            "AesIDu": AesIDu,
            "AesKIu": AesKIu,
            "Tncc": Tncc,
            "HMAC": HMAC
        }
    return "0"



# 处理options['Len_Ru']
def getRandom():
    options = get_options()
    if options['Len_Ru'] == 1: # 16
        return random.randint(1000000000000000, 9999999999999999)
    elif options['Len_Ru'] == 2: # 32
        return random.randint(10000000000000000000000000000000, 99999999999999999999999999999999)
    elif options['Len_Ru'] == 3: # 48
        return random.randint(100000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999)

# 处理options['Hash_option']
def getHash(msg):
    options = get_options()
    if options['Hash_option'] == 1: # sha1
        return hashlib.sha1(msg).hexdigest()
    elif options['Hash_option'] == 2: # sha256
        return hashlib.sha256(msg).hexdigest()
    elif options['Hash_option'] == 3: # sha512
        return hashlib.sha512(msg).hexdigest()

# 处理hmac
def getHmac(MAC_key, msg):
    options = get_options()
    if options['Hash_option'] == 1: # sha1
        return hmac.new(MAC_key, msg, hashlib.sha1).hexdigest()
    elif options['Hash_option'] == 2: # sha256
        return hmac.new(MAC_key, msg, hashlib.sha256).hexdigest()
    elif options['Hash_option'] == 3: # sha512
        return hmac.new(MAC_key, msg, hashlib.sha512).hexdigest()

# 处理options['Key_option']
def encryptData(data, key):
    options = get_options()
    if options['Key_option'] == 1: # AES
        return aes_encrypt(data, key)
    elif options['Key_option'] == 2: # DES
        return des_encrypt(data, key)
    elif options['Key_option'] == 3: # 3DES
        return three_des_encrypt(data, key)

def decryptData(data, key):
    options = get_options()
    if options['Key_option'] == 1: # AES
        return aes_decrypt(data, key)
    elif options['Key_option'] == 2: # DES
        return des_decrypt(data, key)
    elif options['Key_option'] == 3: # 3DES
        return three_des_decrypt(data, key)
