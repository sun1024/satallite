# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory
from flask_cors import CORS
import json
import webbrowser

from dealRequest import *

sessions = {}
sessions["01"] = {
    "IDu":"test",
    "Ku":"test",
    "sessionKey":"test",
    "sessionMACKey":"test",
    "time":int(time.time())
}

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 认证结果展示
@app.route('/authResult', methods=['GET', 'POST'])
def authResult():
    return json.dumps(sessions)

# 卫星展示界面
@app.route('/reqImg', methods=['GET', 'POST'])
def reqImg():
    with open("sate.png", "rb") as img:
        img_content = img.read()
    return img_content

# 卫星展示界面
@app.route('/')
def index():
    # with open("conn.json", "r") as conn:
        # conn_data = json.load(conn)

    # return render_template('index.html', conn_data = conn_data)
    # return app.send_static_file('demo/index.html')
    return app.send_static_file('index.html')


# 卫星收到用户发来的认证信息，连同自己的认证信息一起发给ncc
@app.route('/reqAuth', methods=['GET', 'POST'])
def reqAuthFromUser():
    satalliteData = getReqAuthData()
    satalliteData = json.loads(satalliteData)
    # 这里要对用户信息做出判断
    if(request.data):
        userData = json.loads(request.data)
        try:
            data = sendToNcc(satalliteData, userData)
            return json.dumps(data)
        except Exception, e:
            print e
            data = json.dumps({"ReqAuth":"500"})
            return Response(status=500, response=data)
    else:
        return Response(status=500)


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:2333")
    app.run(
    debug = True,
    port = 2333,
    host = '0.0.0.0'
)