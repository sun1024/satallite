# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory, abort
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import webbrowser

from dealRequest import *
from gl import *



app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return 'NCC'


# 接收卫星发来的satalliteData, userData
@app.route('/identityCheck', methods=['GET', 'POST'])
def identityCheck():
    # 取post信息做验证
    if(request.data):
        # clear_and_add(request.data)
        data = json.loads(request.data)
        try:
            userData = data['userData']
            satalliteData = data['satalliteData']
            # load 认证信息
            userData = json.loads(userData)
            satalliteData = json.loads(satalliteData)
        except Exception, e:
            return json.dumps({
                'Code':"1"
            }), 500

        # 处理认证选项
        try:
            new_options = userData['options']
            # new_options = {
            #     'Hash_option': 1,
            #     'Key_option': 1,
            #     'Len_Ru': 2,
            #     'Zip': 0
            # }
        except Exception, e:
            pass
        else:
            change_options(new_options)

        # 认证用户和卫星
        masterKey = authCheck(userData, satalliteData)
        if masterKey == '0':
            return json.dumps({
                'Code':"1"
            }), 500
        
        retData = retSatallite(masterKey)
        return json.dumps(retData)
    else:
        return 'invalide method', 500


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:2333")
    app.run(
    # debug = True,
    port = 7543,
    host = '0.0.0.0'
)