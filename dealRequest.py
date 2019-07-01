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

    # 计算出IDu、IDs
    IDu = xor_decrypt(PIDu, Hu) 
    IDs = xor_decrypt(PIDs, Hs) 
    # print IDu, IDs

    # 查询出IDu, IDs对应的信息
    # real_sata_data = getAuthData(IDs)
    # real_user_data = getAuthData(IDu)
    real_sata_data = {
        "userId": "06fa43a4b4a63b622e36e3cd4ef55fcfec070b97",
        "userKey": "580ade0f132b4228ea4fe1a289f318f2402fdcd2682ed057a3785fed4312f9f3",
        "preRandom": "55868018469076085065818153351715"
        }
    real_user_data = {
        "userId": "ff4b43ede3bfdaa52ea7f97593f8897fd9a41645",
        "userKey": "124640bf2792a0cdce2c04e13326d67bf013bac6ce546616b04888e7c4e68631",
        "preRandom": "93103486375219430322734306483245"
    }

    # 计算出Rs, Ru
    tmp = getHash(real_sata_data['userKey'] + real_sata_data['preRandom'])
    Rs = xor_decrypt(rs, tmp)
    tmp = getHash(real_user_data['userKey'] + real_user_data['preRandom'])
    Ru = xor_decrypt(ru, tmp)
    
    # 验证MACs MACu
    real_MACs = getHash(real_sata_data['userId'] + Rs + Ts)
    real_MACu = getHash(real_user_data['userId'] + Ru + Tu)

    if MACu == real_MACu and MACs == real_MACs:
        masterKey = getHash(real_user_data['userKey'] + real_sata_data['preRandom'] + Rs)
    return masterKey

# 返回认证信息
def retSatallite(masterKey):
    sign = rsa_sign(masterKey).encode('hex')
    return {
        "Code": "0",
        "Signiture": sign,
        "MasterKey": masterKey
    }

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
