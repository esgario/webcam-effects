import abc
from queue import Queue, Full
from threading import Thread


class Pipeline:
    """
    Pipeline Class responsible to create a chain of connected processes.

        For example, if you have three process [p1, p2 and p3] then you can instantiate your processes stack as:
            Pipeline([p1, p2, p3])

            which results in the follow chain:
            p1 >> p2 >> p3 ...

            where process 'p1' will receive the input data and the 'p3' will produce the output data.

        obs: All processes must inherit from class PipelineStep.

    Usage Example:
        class Square(PipelineStep):
            def __init__(self):
                PipelineStep.__init__(self)

            def handle_message(self, data):
                yield data ** 2

        class Print(PipelineStep):
            def __init__(self):
                PipelineStep.__init__(self)

            def handle_message(self, data):
                print(data)
                yield None

        pipeline = Pipeline([
            Square(),
            Print()
        ])

        pipeline.start()
        pipeline.send_data(10)
        pipeline.join()

    """

    def __init__(self, process_stack):
        self.process_stack = process_stack
        self.num_process = len(self.process_stack)

        # Register watchers
        for i in range(self.num_process - 1):
            self.process_stack[i].register_watcher(self.process_stack[i + 1])

    def start(self):
        for i in range(self.num_process):
            self.process_stack[i].start()

    def send_data(self, data):
        return self.process_stack[0].send_message(data)

    def join(self):
        self.process_stack[0].signalize_eof()
        for i in range(self.num_process):
            self.process_stack[i].join()


class PipelineStep(Thread):
    __metaclass__ = abc.ABCMeta

    def __init__(self, queue_size=2):
        Thread.__init__(self)
        self.queue = Queue(queue_size)
        self.watchers = []

    def get_message(self):
        return self.queue.get()

    def send_message(self, message):
        try:
            self.queue.put(message, block=False)
        except Full:
            return False
        return True

    def register_watcher(self, watcher):
        self.watchers.append(watcher)

    def broadcast_message(self, message):
        for watcher in self.watchers:
            watcher.send_message(message)

    def signalize_eof(self):
        while not self.send_message("eof"):
            continue

    def is_eof(self, message):
        if isinstance(message, str) and message == "eof":
            return True
        return False

    @abc.abstractmethod
    def handle_message(self, message):
        # Handle received message. Abstract metod.
        return

    def run(self):
        while True:
            message = self.get_message()
            if self.is_eof(message):
                self.broadcast_message("eof")
                break
            else:
                for result in self.handle_message(message):
                    if result is None:
                        continue
                    self.broadcast_message(result)
