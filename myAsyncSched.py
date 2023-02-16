import threading
import sched, time


# Класс, выводящий температуру воды в чайнике
class myAsyncSched(object):
    """Asynchronous scheduler"""
    def __init__(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.e = threading.Event()
        self._stop = threading.Event()
        self.start = time.time()

    def addTask(self, delay, task, *args):
        """Add a new task to the scheduler."""
        self.s.enter(delay, 1, task, argument=args, kwargs={'start': self.start})
        self.e.set()

    def stop(self):
        """Stop the scheduler."""
        self._stop.set()
        self.e.set()

    def rmTask(self, arg):
        """Remove a task from the scheduler."""
        for event in self.s.queue:
            if event.argument[0] == arg:
                self.s.cancel(event)

    def run(self):
        """Executes the main loop of the scheduler.
        This is to be executed in a new thread."""
        max_wait = None
        while not self._stop.is_set():
            self.e.wait(max_wait)
            self.e.clear()
            max_wait = self.s.run(blocking=False)