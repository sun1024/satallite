# -*- coding: utf-8 -*-
import time, random
import json, hashlib, requests
import hmac

from xor1 import *
from AES_use import *


# 卫星第一次请求需要的所有数据
def getReqAuthData():
    timestamp = int(time.time())
    Ru = random.randint(1000000000, 9999999999)
    # 读取用户信息
    with open("userInfo.json", "r") as userInfo:
        userInfo = json.load(userInfo)

    H = hashlib.sha256(userInfo["userKey"] + str(timestamp)).hexdigest()
    H = xor_encrypt(userInfo["preRandom"], H)
    PIDu = xor_encrypt(str(userInfo["userId"]), H)
    MACu = hashlib.sha256(userInfo["userId"] + str(Ru) +str(timestamp)).hexdigest()
    ru = hashlib.sha256(userInfo["userKey"] + userInfo['preRandom']).hexdigest()
    ru = xor_encrypt(str(Ru), ru)

    return json.dumps(
        {
            "Ts":str(timestamp),
            "Hs":H,
            "PIDs":PIDu,
            "MACs":MACu,
            "R": Ru,
            "Rs":ru
        }
    )

def sendToNcc(satalliteData, userData):
    #将认证信息传递给ncc
    data = json.dumps({
        "ReqAuth":"ReqAuth",
        "userData":userData,
        "satalliteData":satalliteData
    })
    url = "http://ncc"
    # url = "http://172.33.15.36:7543/index"
    proxies = {'http': 'http://127.0.0.1:8080'}
    reps = requests.post(url, data=data, proxies=proxies)
    # reps = requests.post(url, data=data)
    auth_reps = json.loads(reps.content)
    print auth_reps
    # 通过auth_reps判断认证是否成功

    # return dealResNcc(auth_reps, satalliteData["Rs"], userData["Ru"], userData["PIDu"])

# 处理Ncc返回信息
def dealResNcc(auth_reps, Rs, Ru, PIDu):
    timestamp = int(time.time())

    # 验证签名
    # sign = auth_reps["sign"]

    # 读取用户信息
    with open("userInfo.json", "r") as userInfo:
        userInfo = json.load(userInfo)
    masterKey = auth_reps["masterKey"]
    # 生成sk, MAC_key
    sk = hashlib.sha256(masterKey + userInfo["userKey"]).hexdigest()
    MAC_key = hashlib.sha256(userInfo["userKey"] + masterKey + Rs).hexdigest()
    # 生成MAC
    msg = "ReqUserInfo" + str(timestamp) + PIDu
    MAC = hmac.new(MAC_key, msg, hashlib.sha256)
    # 请求用户身份信息
    url = "http://ncc/reqUserInfo"
    data = json.dumps({
        "ReqAuth":"ReqUserInfo",
        "Ts":str(timestamp),
        "PIDu":PIDu,
        "MAC":MAC
    })
    reps = requests.post(url, data=data)
    auth_reps = json.loads(reps.content)
    # 返回信息：Esk{IDui，Ki}、MAC、TNCC
    return sendToUser(auth_reps, sk, MAC_key, Ru)

# 处理卫星第二次返回的信息：Esk{IDu，Ku}、MAC、TNCC，并返回给用户
def sendToUser(auth_reps, sk, MAC_key, Ru):
    # 从auth_reps中取出MAC, 用MAC_key进行验证
    msg = auth_reps["data1"] + auth_reps["data2"] + auth_reps["Tncc"]
    MAC_compare = hmac.new(MAC_key, msg, hashlib.sha256)

    if(MAC_compare == auth_reps["MAC"]):
        
        # 用sk解密出用户IDu、Ku, 并进行保存
        IDu = aes_decrypt(auth_reps['data1'], sk)
        Ku = aes_decrypt(auth_reps['data2'], sk)

        # 读取用户信息
        with open("userInfo.json", "r") as userInfo:
            userInfo = json.load(userInfo)

        # 计算MAC_user_key, Hsat
        MAC_user_key = hashlib.sha256(IDu + Ku + Ru).hexdigest()
        Hsat = hashlib.sha256(userInfo["userKey"] + userInfo["preRandom"] + Ru).hexdigest()

        # 将Eku(Hsat)，MAC发给用户
        secret = aes_encrypt(Hsat, Ku)
        msg = "ReqUserSSuccess" + secret
        MAC = hmac.new(MAC_user_key, secret, hashlib.sha256)
        data = {
            "ReqAuth":"ReqUserSuccess",
            "secret":secret,
            "MAC":MAC
        }

        # 返回用户
        return data

        
