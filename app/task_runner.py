from queue import Queue
from threading import Thread, Event
from os import environ, cpu_count

class ThreadPool:
    def __init__(self, tasks: list = []):
        self.tasks = tasks

        if environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = environ.get('TP_NUM_OF_THREADS')
        else:
            self.num_threads = cpu_count()
        
        self.queue = Queue()
        self.threads = [TaskRunner(self.tasks, self.queue) for i in range(self.num_threads)]
        for thread in self.threads:
            thread.start()

    def shutdown(self):
        self.queue.join()
        for thread in self.threads:
            thread.shutdown = True
            thread.join()


class TaskRunner(Thread):
    def __init__(self, tasks: list, queue: Queue):
        Thread.__init__(self)
        self.tasks = tasks
        self.queue = queue
        self.shutdown = False
    
    def run(self):
        while True:
            try:
                job = self.queue.get(block=True, timeout=1)
                with open(f'results/{job[0]}', 'a') as f:
                    f.write(job[1]())
                self.queue.task_done()
                self.tasks.append(job[0])
            except Exception as e:
                if self.shutdown:
                    break