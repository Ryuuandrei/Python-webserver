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
            """
            Shuts down the task runner by joining all the threads and stopping their execution.

            This method waits for all the tasks in the queue to be processed and then stops all the threads
            by setting their `shutdown` flag to True and joining them.

            """
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
            """
            Executes the tasks in the queue until the shutdown flag is set.

            This method continuously retrieves tasks from the queue, executes them, and writes the results to the corresponding files.
            If an exception occurs during task execution, it is caught and the loop continues.
            The method also appends the completed task to the list of tasks.

            Note: This method will block if the queue is empty, waiting for new tasks to be added.

            Returns:
                None
            """
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
