#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0
import time

sessions = {}
conns = []

# 处理全局变量conns
def clear_and_add(data):
    if len(conns) != 0:
        del conns[0]
    conns.append(data)
    time.sleep(2)

# 处理全局变量sessions
def add_session(key, value):
    sessions[key] = value

def get_sessions():
    return sessions
