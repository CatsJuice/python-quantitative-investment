import threading

class Threads(object):

    def __init__(self, call_func, thread_num=1, args=None, timeout=0):
        self.call_func = call_func
        self.thread_num = thread_num
        self.args = args

    def create_sub_threads(self):
        pass