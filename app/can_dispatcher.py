from queue import Empty
import threading


class CANDispatcher:
    """
       Диспетчер CAN сообщений.
       Получает сообщения из очереди и распределяет их между зарегистрированными слушателями.
       Работает в отдельном потоке.
   """
    def __init__(self, queue):
        self.listeners = []
        self.queue = queue
        self.thread = None
        self.running = False

        self.QUEUE_TIMEOUT = 0.1
        self.THREAD_STOP_TIMEOUT = 1.0


    def add_listener(self, listener):
            self.listeners.append(listener)


    def add_listeners(self, listeners):
        if isinstance(listeners, list):
            self.listeners.extend(listeners)
        else:
            self.listeners.append(listeners)
        return self.listeners

    def remove_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)


    def _dispatch_loop(self):
        while self.running:
            try:
                message = self.queue.get(timeout=self.QUEUE_TIMEOUT)

            except Empty:
                continue

            try:
                for listener in self.listeners:
                    listener.handle_frame(message)

            except Exception as e:
                print(f"Ошибка в слушателе: {e}")

            finally:
                self.queue.task_done()


    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.running = True
        self.thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=self.THREAD_STOP_TIMEOUT)

            if self.thread.is_alive():
                print("Warning: receiver thread did not stop")

        self.thread = None
