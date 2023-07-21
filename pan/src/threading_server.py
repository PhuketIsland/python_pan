import socket
import select
import threading
from config import settings


class SelectServer(object):
    def __init__(self):
        self.host = settings.HOST
        self.port = settings.PORT
        self.socket_object_list = []
        self.conn_handler_map = {}
        self.lock = threading.Lock()

    def handle_new_connection(self, server_object, handler):
        while True:
            conn, addr = server_object.accept()
            with self.lock:
                print("新客户端来连接")
                self.socket_object_list.append(conn)
                self.conn_handler_map[conn] = handler(conn)

    def run(self, handler):
        server_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_object.setblocking(True)
        server_object.bind((self.host, self.port))
        server_object.listen(5)
        self.socket_object_list.append(server_object)

        new_conn_thread = threading.Thread(target=self.handle_new_connection, args=(server_object, handler))
        new_conn_thread.start()

        while True:
            with self.lock:
                r, _, _ = select.select(self.socket_object_list, [], [], 0.05)
                for sock in r:
                    # 新数据到来，执行 handler 的 execute 方法
                    handler_object = self.conn_handler_map[sock]
                    # 执行 handler 类对象的 execute 方法，如果返回 False，则意味关闭服务端与客户端的连接
                    result = handler_object.execute()
                    if not result:
                        sock.close()
                        self.socket_object_list.remove(sock)
                        del self.conn_handler_map[sock]

