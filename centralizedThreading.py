import threading
import multiprocessing
import traceback
import logging


class FunctionNameAlreadyExists(Exception):
    def __init__(self, eventName):
        self.name = eventName
    def __str__(self):
        return self.name
    
class ThreadTemplate(threading.Thread):
    def __init__(self, name, function, pipe_Thread, pipe_Main, baseReference = None):
        threading.Thread.__init__(self)
        self.function = function
        self.name = name
        
        # MainPipe and ThreadPipe are the two ends of the same pipe. 
        # Data sent on MainPipe can be received on ThreadPipe, and vice versa.
        # MainPipe is used by the bot framework. ThreadPipe is used by the thread.
        self.MainPipe = pipe_Main
        self.ThreadPipe = pipe_Thread
        
        self.running = False
        self.signal = False
        
        self.base = baseReference
        
    def run(self):
        self.running = True
        try:
            self.function(self, self.ThreadPipe)
        except Exception as error:
            self.ThreadPipe.send({
                                  "action" : "exceptionOccured", "exception" : error, 
                                  "functionName" : self.name, "traceback" : str(traceback.format_exc())
                                  })
            
        self.running = False


class ThreadPool():
    def __init__(self):
        self.pool = {}
        self.__threadPool_log__ = logging.getLogger("ThreadPool")
        
    def addThread(self, name, function, baseReference = None):
        MainPipe, ThreadPipe = multiprocessing.Pipe(True)
        
        if name in self.pool:
            raise FunctionNameAlreadyExists("The name is already used by a different thread function!")
        
        thread = ThreadTemplate(name, function, ThreadPipe, MainPipe, baseReference)
        self.pool[name] = {"thread" : thread, "threadPipe" : ThreadPipe, "mainPipe" : MainPipe}
        self.pool[name]["thread"].start()
        self.__threadPool_log__.debug("New thread '%s' started", name)
    
    def sigquitThread(self, name):
        self.pool[name]["thread"].signal = True
        del self.pool[name]
        self.__threadPool_log__.debug("Sending SIGKILL to thread '%s'", name)
    
    def send(self, name, obj):
        self.pool[name]["mainPipe"].send(obj)
    
    def recv(self, name):
        return self.pool[name]["mainPipe"].recv()
    
    def poll(self, name, timeout = 0.1):
        return self.pool[name]["mainPipe"].poll(timeout)
        
    
    def sigquitAll(self):
        self.__threadPool_log__.debug("Sending SIGKILL to all running threads")
        threads = [name for name in self.pool]
        
        for thread in threads:
            self.pool[thread]["thread"].signal = True
            del self.pool[thread]
        
        self.__threadPool_log__.debug("SIGKILL to all running threads sent")
        
        