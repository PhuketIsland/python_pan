from src.handlers.pan import PanHandler
from src.select_server import SelectServer
from src.threading_server import SelectServer

if __name__ == '__main__':
    # server = SelectServer()
    # server.run(PanHandler)
    thread_server = SelectServer()
    thread_server.run(PanHandler)