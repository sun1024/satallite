# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory, abort
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import webbrowser

from dealRequest import *
from gl import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
CORS(app, supports_credentials=True)

# 创建表格、插入数据
@app.before_first_request
def create_db():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()
    test = User('0', 'test', 'test', 'test')
    db.session.add(test)
    users = [User(
        '0',
        '06fa43a4b4a63b622e36e3cd4ef55fcfec070b97', 
        '580ade0f132b4228ea4fe1a289f318f2402fdcd2682ed057a3785fed4312f9f3',
        '55868018469076085065818153351715'
        ),
        User(
        '1',
        'ff4b43ede3bfdaa52ea7f97593f8897fd9a41645', 
        '124640bf2792a0cdce2c04e13326d67bf013bac6ce546616b04888e7c4e68631',
        '93103486375219430322734306483245'
        )]
    db.session.add_all(users)
    db.session.commit()

@app.route('/')
def index():
    return 'NCC'

@app.route('/reqUserInfo', methods=['GET', 'POST'])
def reqUserInfo():
    if(request.data):
        try:
            data = json.loads(request.data)
            retUserInfo = getUserInfo(data)
            return json.dumps(retUserInfo)
        except Exception, e:
            print e
            return "someting error...", 500
            
    return 'tbc', 500

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
        except Exception, e:
            print e
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
            # print e
        else:
            change_options(new_options)

        # 认证用户和卫星
        try:
            masterKey = authCheck(userData, satalliteData)
            if masterKey == '0':
                return json.dumps({
                    'Code':"1"
                }), 500
            
            retData = retSatallite(masterKey)
            return json.dumps(retData)
        except Exception, e:
            print e
            return json.dumps({
                'Code':"1"
            }), 500
    else:
        return 'invalide method', 500


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:2333")
    app.run(
    debug = True,
    port = 7543,
    host = '0.0.0.0'
)