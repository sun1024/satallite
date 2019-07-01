#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0
import time

sessions = {}
conns = []
options = {
    'Hash_option': 2,
    'Key_option': 1,
    'Len_Ru': 2,
    'Zip': 0
}

# 处理全局变量conns
def clear_and_add(data):
    if len(conns) != 0:
        del conns[0]
    conns.append(data)
    time.sleep(2)

# 处理全局变量sessions
def add_session(key, value):
    sessions[key] = value

def get_sessions(PIDu):
    keys = sessions[PIDu]

    return keys['sk'], keys['MAC_Key']

# 处理全局变量options
def get_options():
    return options

def set_options(key, value):
    options[key] = value

def change_options(new_options):
    global options
    options = new_options