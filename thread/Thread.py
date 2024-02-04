import threading
from queue import Queue


class CustomThread(threading.Thread):
    def __init__(self, queue, **kwargs):
        super(CustomThread, self).__init__(**kwargs)
        self.__queue = queue
        self.__results = []

    def run(self):
        while True:
            try:
                item = self.__queue.get()
                self.__results.append(item[0](*item[1:]))
                self.__queue.task_done()
            except Exception as e:
                print(f'WORK ERROR,err: {e}')
                self.__queue.task_done()

    def get_result(self):
        try:
            return self.__results
        except Exception:
            return None


class ThreadPool():
    def __init__(self, max_thread, max_queue):
        self.__max_workers = max_thread
        self.__queue = Queue(maxsize=max_queue)
        self.__threads = []
        self.start()

    def start(self):
        for _ in range(self.__max_workers):
            t = CustomThread(self.__queue, daemon=True)
            t.start()
            self.__threads.append(t)

    def add_task(self, *args):
        self.__queue.put(*args, block=True)

    def wait(self):
        self.__queue.join()

    def get_results(self):
        results = []
        for thread in self.__threads:
            results.extend(thread.get_result())
        return results
