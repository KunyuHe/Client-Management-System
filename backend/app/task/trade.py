from datetime import datetime
from threading import Lock

from app.models.model import Client
from app.utils.core import db
from flask_socketio import Namespace, join_room, leave_room

THREAD = None
THREAD_LOCK = Lock()
CONNECTIONS = 0


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        TradeNamespace.get_socketio().sleep(5)
        with db.app.app_context():
            try:
                to_notify = Client.query.filter(Client.trade == True).all()
                if not to_notify:
                    continue

                for client_obj in to_notify:
                    now = datetime.now().strftime('%Y-%m-%d %I:%M %p')
                    for user_obj in client_obj.users:
                        TradeNamespace.get_socketio().emit(
                            'hi', f"客户{client_obj.name}于{now}提出交易需求",
                            room=user_obj.name, namespace="/flask")
                    client_obj.trade = False
                db.session.commit()
            except Exception as ex:
                logger.error(ex)


class TradeNamespace(Namespace):
    __socketio__ = None

    @classmethod
    def set_socketio(cls, socketio):
        cls.__socketio__ = socketio

    @classmethod
    def get_socketio(cls):
        return cls.__socketio__

    def on_connect(self):
        global THREAD, THREAD_LOCK, CONNECTIONS
        with THREAD_LOCK:
            CONNECTIONS += 1
            if (THREAD is None) or (not THREAD.is_alive()):
                THREAD = TradeNamespace.get_socketio().start_background_task(
                    background_thread)

    def on_disconnect(self):
        global THREAD_LOCK, CONNECTIONS
        with THREAD_LOCK:
            CONNECTIONS -= 1

    def on_join(self, data):
        global THREAD_LOCK
        with THREAD_LOCK:
            join_room(room=data['user']['name'], namespace="/flask")

    def on_leave(self, data):
        global THREAD_LOCK
        with THREAD_LOCK:
            leave_room(room=data['user']['name'], namespace="/flask")
