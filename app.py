# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request, render_template, Response, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import webbrowser

from dealRequest import *
from gl import *


# sessions["06fa43a4b4a63b622e36e3cd4ef55fcfec070b97"] = {
#     "IDu":"test",
#     "Ku":"test",
#     "sessionKey":"580ade0f132b4228ea4fe1a289f318f2402fdcd2682ed057a3785fed4312f9f3",
#     "sessionMACKey":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
#     "time":int(time.time())
# }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, supports_credentials=True)

socketio = SocketIO(app)

@app.route('/')
def index():
    # return render_template('test.html')
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


# 认证结果展示
@app.route('/authResult', methods=['GET', 'POST'])
def authResult():
    sessions = get_sessions()
    sessionId = sessions.keys()[0]
    return json.dumps({
        "sessionId":sessionId,
        "sessionKey":sessions[sessionId]["sessionKey"],
        "MACKey":sessions[sessionId]["sessionMACKey"]
    })

# 用户请求卫星文件
@app.route('/reqImg', methods=['GET', 'POST'])
def reqImg():
    with open("sate.png", "rb") as img:
        img_content = img.read()
    # 对图像信息进行加密
    if img_content:
        try:
            data = json.loads(authResult())
            reps = imgRepo(data, img_content)
            return reps
        except Exception, e:
            print e
            return "0"

    return "1"

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     with open('conn.log', 'r') as conn:
#         resp = {}
#         index = 1
#         while 1:
#             conn_data = conn.readline()[:-1]
#             if not conn_data:
#                 break
#             resp[index] = conn_data
#             index += 1

#     return json.dumps(resp)

# 卫星展示界面
@app.route('/old', methods=['GET', 'POST'])
def index_old():
    # with open("conn.json", "r") as conn:
        # conn_data = json.load(conn)

    # return render_template('index.html', conn_data = conn_data)
    # return app.send_static_file('demo/index.html')
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
            new_options_exists = False
        else:
            new_options_exists = True
        if new_options_exists:
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
    # sessions = {}
    # conns = []
    # webbrowser.open("http://127.0.0.1:2333")
#     app.run(
#     # debug = True,
#     port = 2333,
#     host = '0.0.0.0'
# )
    socketio.run(
        app,
        # debug=True,
        host='0.0.0.0',
        port=2333
        )