from queue import Queue
from threading import Thread, Event
import time
from os import environ, cpu_count

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        if environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = environ.get('TP_NUM_OF_THREADS')
        else:
            self.num_threads = cpu_count()
        
        self.queue = Queue()
        self.num_threads = [TaskRunner(i, self.queue) for i in range(self.num_threads)]
        for thread in self.num_threads:
            thread.start()

class TaskRunner(Thread):
    def __init__(self, thread_id: int, queue: Queue):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
    
    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            job = self.queue.get()
            with open(f'results/{job[0]}', 'a') as f:
                f.write(job[1]())
            self.queue.task_done()
