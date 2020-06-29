import logging
from threading import Lock

from flask_socketio import Namespace, emit

logger = logging.getLogger(__name__)

thread = None
thread_lock = Lock()


def background_thread():
    pass


class TradeNamespace(Namespace):
    __send_time__ = None
    __socketio__ = None

    @classmethod
    def set_send_time(cls, time):
        cls.__send_time__ = time

    @classmethod
    def get_send_time(cls):
        return cls.__send_time__

    @classmethod
    def set_socketio(cls, socketio):
        cls.__socketio__ = socketio

    @classmethod
    def get_socketio(cls):
        return cls.__socketio__

    def on_connect(self):
        global thread, thread_lock
        with thread_lock:
            if (thread is None) or (not thread.is_alive()):
                thread = TradeNamespace.get_socketio().start_background_task(
                    background_thread)

    def on_disconnect(self):
        global thread, thread_lock, connections
        with thread_lock:
            pass

    def on_reconnect(self):
        global thread
        with thread_lock:
            if connections >= 0:
                if not thread.is_alive():
                    thread = TradeNamespace.get_socketio().start_background_task(
                        background_thread())

    def on_my_event(self, data):
        emit('hi', data)
