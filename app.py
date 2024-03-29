# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory, abort
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import webbrowser

from dealRequest import *
from gl import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, supports_credentials=True)

socketio = SocketIO(app)

@app.route('/')
def index():
    # return app.send_static_file('show.html')
    return app.send_static_file('display/index.html')

@app.route('/show')
def show():
    return app.send_static_file('show.html')


@socketio.on('client_event')
def client_msg(msg):
    # emit('server_response', {'data': msg['data']})
    while 1:
        global conns
        emit('server_response', {'data': conns})
        time.sleep(0.5)
    

# 用户请求卫星图片
@app.route('/reqImg', methods=['GET', 'POST'])
def reqImg():
    if(request.data):
        sessionId = json.loads(request.data)["sessionId"]

        sessions = get_sessions()
        try:
            session_data = sessions[sessionId]
            # 判断session是否过期
            now = int(time.time())
            if now-session_data['time'] > 60*30:
                return "expire", 401

            IDu = session_data['IDu']
            userData = json.dumps({
                'IDu': IDu,
                'sessionId': sessionId,
                'ReqAuth': 'reqImg'
            })
            clear_and_add(userData)
        except KeyError:
            return 'you not auth success', 500
        
        with open("static/img/sate.png", "rb") as img:
            img_content = img.read()
        # 对图像信息进行加密
        if img_content:
            try:
                data = authResult(sessionId)
                return imgRepo(data, img_content)
            except Exception, e:
                print e
                imgError = json.dumps({
                    'error': e,
                    'ReqAuth': 'imgError',
                    'IDu': IDu
                })
                clear_and_add(imgError)
                return "img crypty error", 500

    return "method error", 500

# 认证成功访问页面
@app.route('/success', methods=['GET', 'POST'])
def success():
    # if request.method == 'POST':
    if(request.data):
        try:
            sessionId = json.loads(request.data)["sessionId"]
            temp_sessions = get_sessions()
            # session_data = temp_sessions[sessionId]
            session_data = temp_sessions.get(sessionId)
            # 判断session是否过期
            now = int(time.time())
            if now-session_data['time'] < 60*30:
                return '200'

            return "expire", 401
        except Exception, e:
            print e
            return "500", 500

    return "500", 500



# 卫星收到用户发来的认证信息，连同自己的认证信息一起发给ncc
@app.route('/reqAuth', methods=['GET', 'POST'])
def reqAuthFromUser():

    # 这里要对用户信息做出判断
    if(request.data):
        userData = json.loads(request.data)
        # 粗糙的验证用户信息
        if not user_valid(userData):
            return 'timeout', 500
        # 统计接入用户
        global conn_user
        global succ_user
        conn_user += 1
        userData['conn_user'] = conn_user
        userData['succ_user'] = succ_user
        clear_and_add(json.dumps(userData))
        # 处理认证选项
        try:
            new_options = userData['Options']
            # new_options = {
            #     'Hash_option': 1,
            #     'Key_option': 1,
            #     'Len_Ru': 2,
            #     'Zip': 0
            # }
        except Exception, e:
            print "no options from user"
            pass
        else:
            change_options(new_options)
        # 获取卫星认证数据
        print get_options()
        satalliteData = getReqAuthData()
        satalliteData = json.loads(satalliteData)

        # sendToNcc
        try:
            data = sendToNcc(satalliteData, userData)
            # 统计成功信息
            succ_user += 1
            data['conn_user'] = conn_user
            data['succ_user'] = succ_user
            data = json.dumps(data)
            clear_and_add(data)
            return data
        except Exception, e:
            print e
            data = json.dumps({
                "ReqAuth":"500",
                "PIDu":userData["PIDu"],
                "conn_user": conn_user,
                "succ_user": succ_user
                })
            clear_and_add(data)
            return Response(status=500, response=data)
    else:
        return Response(status=500)

# 二次认证
@app.route('/secondAuth', methods=['GET', 'POST'])
def secondAuth():
    # 接收认证数据
    if request.data:
        try:
            data = json.loads(request.data)
            return dealSecondAuth(data)
        except Exception, e:
            print e
            data = json.dumps({
                "RepAuth":"500",
                })
            clear_and_add(data)
            return 'auth error', 500
    else:
        return 'method error', 500

@app.route('/getUserList', methods=['GET', 'POST'])
def getUserList():
    temp_sessions = get_sessions()
    return json.dumps(temp_sessions)


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:2333")
    socketio.run(
        app,
        # debug=True,
        host='0.0.0.0',
        port=2333
        )