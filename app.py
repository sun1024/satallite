# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
import json, hashlib, random, time, hmac
import requests

from xor1 import *
from AES_use import *

sessions = {}
sessions["06fa43a4b4a63b622e36e3cd4ef55fcfec070b97"] = {
    "IDu":"test",
    "Ku":"test",
    "sessionKey":"580ade0f132b4228ea4fe1a289f318f2402fdcd2682ed057a3785fed4312f9f3",
    "sessionMACKey":hashlib.sha256("test").hexdigest(),
    "time":int(time.time())
}

app = Flask(__name__)
CORS(app, supports_credentials=True)


# 用户第一次请求需要的所有数据
def getReqAuthData():
    timestamp = int(time.time())
    # 32
    Ru = random.randint(10000000000000000000000000000000, 99999999999999999999999999999999)
    # 读取用户信息
    with open("userInfo.json", "r") as userInfo:
        userInfo = json.load(userInfo)

    H = hashlib.sha256(userInfo["userKey"] + str(Ru)).hexdigest()
    H = xor_encrypt(userInfo["preRandom"], H)
    PIDu = xor_encrypt(str(userInfo["userId"]), H)
    MACu = hashlib.sha256(userInfo["userId"] + str(Ru) +str(timestamp)).hexdigest()
    ru = hashlib.sha256(userInfo["userKey"] + userInfo['preRandom']).hexdigest()
    ru = xor_encrypt(str(Ru), ru)

    return json.dumps(
        {
            "Tu":str(timestamp),
            "Hu":H,
            "PIDu":PIDu,
            "MACu":MACu,
            "Ru":ru
        }
    )

# 用户向卫星发起第一次请求
def reqAuth():
    url = "http://127.0.0.1:2333/reqAuth"
    data = getReqAuthData()
    resp = requests.post(url, data=data)
    data =  json.loads(resp.content)
    if data['ReqAuth'] == "500":
        print "failed..."
        return "failed"
    else:
        secretHsat = data["secretHsat"]
        secretSessionId = data["secretSessionId"]
        MAC = data["MAC"]
        # 对MAC进行验证

        # 解开 secretHsat secretSessionId
        with open("userInfo.json", "r") as userInfo:
            userInfo = json.load(userInfo)
        Ku = userInfo["userKey"]
        IDu = userInfo["userId"]
        Ku_use = bytes(Ku.decode('hex'))
        Hsat = decrypt(secretHsat, Ku_use)
        sessionId = decrypt(secretSessionId, Ku_use)


        # 生成会话密钥 sessionKey sessionMACKey
        sessionKey = hashlib.sha256(Hsat + Ku).hexdigest()
        sessionMACKey = hashlib.sha256(IDu + Hsat).hexdigest()

        # global sessions
        # sessions[sessionId] = {
        #     "IDu":IDu,
        #     "Ku":Ku,
        #     "sessionKey":sessionKey,
        #     "sessionMACKey":sessionMACKey,
        #     "time":int(time.time())
        # }

        print sessionKey, sessionMACKey
        print "auth success..."
        return "success"

        # time.sleep(5)
        # # 向卫星请求一张图片
        # reqImg(sessionId, sessionKey, sessionMACKey)


# 认证结果展示
def authResult():
    sessionId = sessions.keys()[0]
    return json.dumps({
        "sessionId":sessionId,
        "sessionKey":sessions[sessionId]["sessionKey"],
        "MACKey":sessions[sessionId]["sessionMACKey"]
    })

# 接收卫星图片
@app.route('/reqImg', methods=['GET','POST'])
def reqImg():
    if(request.data):
        try:
            imgData = json.loads(request.data)
            content = imgData['content']
            sessionId = imgData['sessionId']
            MAC = imgData['MAC']

            # 读取sessions
            data = json.loads(authResult())

            mySessionId = data['sessionId']
            MACKey = bytes(data['MACKey'])
            sessionKey = data["sessionKey"]
            
            # 验证MAC
            myMAC = hmac.new(MACKey, content, hashlib.sha256).hexdigest()
            if MAC == myMAC:
                key_use = bytes(sessionKey.decode('hex'))

                resp = decrypt(content, key_use)
                with open("sate.png", "wb") as img:
                    img.write(resp)
                return "1"
            
            return "0"
        except Exception, e:
            print e
            return "0"

    return "0"


@app.route('/userAuth', methods=['GET','POST'])
def userAuth():
    status = reqAuth()
    return status


def requestUrl(url):
    data = requests.get(url).content
    return json.loads(data)

@app.route('/test', methods=['GET','POST'])
def testJsonRecv():
    url = "http://47.101.217.127:8888/money"
    data = requestUrl(url)
    return json.dumps(data)

if __name__ == "__main__":
    # status = reqAuth()
    # print status
    app.run(
    debug = True,
    port = 8888,
    host = '0.0.0.0'
)