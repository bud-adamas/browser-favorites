#!/usr/bin/env python
# coding: utf-

import socket
import threading
from threading import Thread
import threading
import sys
import time
import random
from Queue import Queue

host = ''
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(3)

class ThreadPoolManager():
    """
    线程池初始化
    """
    def __init__(self, thread_num):
        # 初始化参数
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        # 初始化线程池，创建指定数量的线程池
        for i in range(thread_num):
            thread = ThreadManager(self.work_queue)
            thread.start()

    def add_job(self, func, *args):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((func, args))


class ThreadManager(Thread):
    """初始化线程类，继承 threading.Thread """
    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        # 启动线程
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()

# 创建一个有 4 个线程的线程池
thread_pool = ThreadPoolManager(4)

# 处理 http 请求，这里简单返回 200 hello world
def handle_request(conn_socket):
    recv_data = conn_socket.recv(1024)
    reply = 'HTTP/1.1 200 OK\r\n\r\n'
    reply += 'hello world'
    print 'thread %s is running ' % threading.current_thread().name
    conn_socket.send(reply)
    conn_socket.close()

# 循环等待接近客户端请求
while True:
    # 阻塞等待请求
    conn_socket, addr = s.accept()
    # 一旦有请求，把 socket 扔到我们指定处理函数 handle_request
    # 处理，等待线程池分配线程处理
    thread_pool.add_job(handle_request, *(conn_socket, ))
