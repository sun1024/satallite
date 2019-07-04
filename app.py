# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory
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

    
# @socketio.on('table_event')
# def connected_msg(msg):
#     table = {
#         'user':'IgpX****',
#         'time':'2019-06-27 09:52:38',
#         'status':'请求卫星'
#     }
#     while 1:
#         emit('table_response', {'data': table})
#         time.sleep(0.5)


# 用户请求卫星图片
@app.route('/reqImg', methods=['GET', 'POST'])
def reqImg():
    if request.method == 'POST':
        sessionId = request.form.get('sessionId')

        sessions = get_sessions()
        try:
            session_data = sessions[sessionId]
        except KeyError:
            return 'you not auth success', 500
        
        with open("sate.png", "rb") as img:
            img_content = img.read()
        # 对图像信息进行加密
        if img_content:
            try:
                data = authResult(sessionId)
                reps = imgRepo(data, img_content)
                return reps
            except Exception, e:
                print e
                return "0", 500

    return "1", 500

# 认证成功访问页面
@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        sessionId = request.form.get('sessionId')

        sessions = get_sessions()
        try:
            session_data = sessions[sessionId]
            # return 'user: {} auth success'.format(session_data['IDu'])
            return render_template('failed.html', user=session_data['IDu'])
        except KeyError:
            return render_template('failed.html'), 500

    return render_template('failed.html'), 500

# 卫星展示界面
@app.route('/old', methods=['GET', 'POST'])
def index_old():
    # 处理认证选项
    if request.method == 'POST':
        return app.send_static_file('test.html')

    # return app.send_static_file('index.html')
    return app.send_static_file('display.html')


# 卫星收到用户发来的认证信息，连同自己的认证信息一起发给ncc
@app.route('/reqAuth', methods=['GET', 'POST'])
def reqAuthFromUser():

    # 这里要对用户信息做出判断
    if(request.data):
        clear_and_add(request.data)
        userData = json.loads(request.data)
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
        # 获取卫星认证数据
        satalliteData = getReqAuthData()
        satalliteData = json.loads(satalliteData)

        # sendToNcc
        try:
            data = sendToNcc(satalliteData, userData)
            data = json.dumps(data)
            clear_and_add(data)
            return data
        except Exception, e:
            print e
            data = json.dumps({
                "ReqAuth":"500",
                "PIDu":userData["PIDu"]
                })
            clear_and_add(data)
            return Response(status=500, response=data)
    else:
        return Response(status=500)


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:2333")
    socketio.run(
        app,
        # debug=True,
        host='0.0.0.0',
        port=2333
        )