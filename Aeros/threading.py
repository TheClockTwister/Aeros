import threading
import ctypes


class AdvancedThread(threading.Thread):
    """ This thread class extends the pure-python "Thread" class
    by a stop() function to terminate the thread's run() method. """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

    def __get_id(self):
        """ Get's the threads PID. """
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self):
        """ Sends a kill signal to the given thread """
        thread_id = self.__get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
