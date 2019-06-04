# -*- coding: utf-8 -*-
import time, random
import json, hashlib, requests
import hmac

from xor1 import *
from AES_use import *
from RSA_sign import *

sessions = {}

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
    url = "http://172.23.22.179:7543/ncc/user/IdentityCheck"
    proxies = {'http': 'http://127.0.0.1:8080'}
    reps = requests.post(url, data=data, proxies=proxies)
    # reps = requests.post(url, data=data)
    auth_reps = json.loads(reps.content)
    print auth_reps["MasterKey"]
    if auth_reps["Code"] == "0":
        # 通过auth_reps判断认证是否成功
        return dealResNcc(auth_reps, satalliteData["Rs"], userData["Ru"], userData["PIDu"])
    else:
        data = {"ReqAuth":"ReqAuthFailed"}
        return data


# 处理Ncc返回信息
def dealResNcc(auth_reps, Rs, Ru, PIDu):
    timestamp = int(time.time())

    # 验证签名
    sign = auth_reps["Signiture"].decode('hex')
    verify = rsa_verify(sign, auth_reps["MasterKey"])
    if verify:
        # 读取用户信息
        with open("userInfo.json", "r") as userInfo:
            userInfo = json.load(userInfo)
        masterKey = auth_reps["MasterKey"]
        # 生成sk, MAC_key
        sk = hashlib.sha256(masterKey + userInfo["userKey"]).hexdigest()
        MAC_key = hashlib.sha256(userInfo["userKey"] + masterKey + Rs).hexdigest()
        # 生成MAC
        msg = "ReqUserInfo" + str(timestamp) + PIDu
        MAC = hmac.new(MAC_key, msg, hashlib.sha256).hexdigest()
        # 请求用户身份信息
        url = "http://ncc/reqUserInfo"
        data = json.dumps({
            "ReqAuth":"ReqUserInfo",
            "Ts":str(timestamp),
            "PIDu":PIDu,
            "MAC":str(MAC)
        })
        proxies = {'http': 'http://127.0.0.1:8080'}
        reps = requests.post(url, data=data, proxies=proxies)
        # reps = requests.post(url, data=data)
        auth_reps = json.loads(reps.content)
        # 返回信息：Esk{IDui，Ki}、MAC、TNCC
        # return sendToUser(auth_reps, sk, MAC_key, Ru)
        return "200"
    else:
        data = {"ReqAuth":"ReqAuthFailed"}
        return data

# 处理卫星第二次返回的信息：Esk{IDu，Ku}、MAC、TNCC，并返回给用户
def sendToUser(auth_reps, sk, MAC_key, Ru):
    # 从auth_reps中取出MAC, 用MAC_key进行验证
    msg = auth_reps["data1"] + auth_reps["data2"] + auth_reps["Tncc"]
    MAC_compare = hmac.new(MAC_key, msg, hashlib.sha256).hexdigest()

    if(str(MAC_compare) == auth_reps["MAC"]):
        # 生成sessionId 并保存session
        sessionId = random.randint(1000000000, 9999999999)       
        # 用sk解密出用户IDu、Ku, 并进行保存
        IDu = aes_decrypt(auth_reps['data1'], sk)
        Ku = aes_decrypt(auth_reps['data2'], sk)

        # global sessions
        # sessions[sessionId] = {
        #     "IDu":IDu,
        #     "Ku":Ku
        # }

        # 读取用户信息
        with open("userInfo.json", "r") as userInfo:
            userInfo = json.load(userInfo)

        # 计算MAC_user_key, Hsat
        MAC_user_key = hashlib.sha256(IDu + Ku + Ru).hexdigest()
        Hsat = hashlib.sha256(userInfo["userKey"] + userInfo["preRandom"] + Ru).hexdigest()

        # 将Eku(Hsat)，MAC发给用户
        secretHsat = aes_encrypt(Hsat, Ku)
        secretSessionId = aes_encrypt(sessionId, Ku)
        msg = "ReqUserSSuccess" + secretHsat + secretSessionId
        MAC = hmac.new(MAC_user_key, secretHsat, hashlib.sha256)
        data = {
            "ReqAuth":"ReqUserSuccess",
            "secretHsat":secretHsat,
            "sessionId":secretSessionId,
            "MAC":MAC
        }

        # 生成会话密钥 sessionKey sessionMACKey
        sessionKey = ""
        sessionMACKey = ""

        global sessions
        sessions[sessionId] = {
            "IDu":IDu,
            "Ku":Ku,
            "sessionKey":sessionKey,
            "sessionMACKey":sessionMACKey,
            "time":int(time.time())
        }
        
        # 返回用户
        return data

        
