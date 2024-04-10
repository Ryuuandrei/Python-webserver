"""
Module for the ThreadPool and TaskRunner classes.
"""
from queue import Queue
from threading import Thread
from os import environ, cpu_count, path, makedirs

class ThreadPool:
    """
    A class representing a thread pool for executing tasks concurrently.

    The ThreadPool class manages a pool of threads that can execute tasks in parallel.
    It takes a list of tasks as input and distributes them among the threads for execution.

    Attributes:
        tasks (list): A list of tasks to be executed by the thread pool.
        num_threads (int): The number of threads in the thread pool.
        queue (Queue): A queue to store the tasks.
        threads (list): A list of TaskRunner threads.

    Methods:
        __init__(self, tasks: list = []): Initializes the ThreadPool object.
        shutdown(self): Shuts down the task runner by joining all the threads
        and stopping their execution.
    """

    def __init__(self, tasks: list):
        self.tasks = tasks

        if environ.get('TP_NUM_OF_THREADS') is not None:
            self.num_threads = environ.get('TP_NUM_OF_THREADS')
        else:
            self.num_threads = cpu_count()

        if not path.exists('results'):
            makedirs('results')

        self.queue = Queue()
        self.threads = [TaskRunner(self.tasks, self.queue) for i in range(self.num_threads)]
        for thread in self.threads:
            thread.start()

    def shutdown(self):
        """
        Shuts down the task runner by joining all the threads and stopping their execution.

        This method waits for all the tasks in the queue to be processed and then stops all
        the threads by setting their `shutdown` flag to True and joining them.

        """
        self.queue.join()
        for thread in self.threads:
            thread.shutdown = True
            thread.join()


class TaskRunner(Thread):
    """
    A class representing a task runner that executes tasks in a thread.

    The TaskRunner class is a subclass of the Thread class and is responsible for executing
    tasks in a separate thread. It retrieves tasks from a queue, executes them, and writes
    the results to the corresponding files.

    Attributes:
        tasks (list): A list of tasks to be executed.
        queue (Queue): A queue to store the tasks.
        shutdown (bool): A flag to indicate whether the task runner should be shut down.

    Methods:
        run(self): Executes the tasks in the queue until the shutdown flag is set.
    """

    def __init__(self, tasks: list, queue: Queue):
        """
        Initializes a TaskRunner object.

        Args:
            tasks (list): A list of tasks.
            queue (Queue): A queue to store the tasks.

        Returns:
            None
        """
        Thread.__init__(self)
        self.tasks = tasks
        self.queue = queue
        self.shutdown = False

    def run(self):
        """
        Executes the tasks in the queue until the shutdown flag is set.

        This method continuously retrieves tasks from the queue, executes them,
        and writes the results to the corresponding files. If an exception occurs
        during task execution, it is caught and the loop continues. The method also
        appends the completed task to the list of tasks.

        Note: This method will block if the queue is empty, waiting for new tasks to be added.

        Returns:
            None
        """
        while True:
            try:
                job = self.queue.get(block=True, timeout=1)
                with open(f'results/{job[0]}', 'a', encoding='utf-8') as f_out:
                    f_out.write(job[1]())
                self.queue.task_done()
                self.tasks.append(job[0])
            except Exception:
                if self.shutdown:
                    break
