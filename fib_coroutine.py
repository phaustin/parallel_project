"""Async fibonacci implementation taken from:
http://stackoverflow.com/questions/25105850/asyncio-with-mapreduce-flavor-and-without-flooding-the-event-loop"""     
import asyncio
import sys
from time import time
queue = asyncio.Queue()

def handle_stdin():
    data = sys.stdin.readline()
    asyncio.async(queue.put(data))

@asyncio.coroutine
def coro_sum(summands):
    return sum(summands)

@asyncio.coroutine
def fib(n):
    if n<=1:
        s = n
    else:
        yield from asyncio.sleep(0) #stops the computation from blocking 
        a = yield from fib(n-2) 
        b = yield from fib(n-1) 
        s = yield from coro_sum([a, b])
    return s

def log_execution_time(method):
    """decorator for timing a coroutine""" 
    def timed(*args, **kw):
        ts = time()
        result = yield from method(*args, **kw)
        te = time()
        print('%r %2.2f sec' % \
              (method.__name__, te-ts))
        return result
    return timed

timed_fib = log_execution_time(fib)               

def tick():
    while True:
       text = yield from queue.get()
       n = int(text.strip())
       res = yield from timed_fib(n)
       print('fib({}) = {}'.format(n, res))


@asyncio.coroutine
def print_hello():
    while True:
        print("{} - Hello world!".format(int(time())))
        yield from asyncio.sleep(3)    

loop = asyncio.get_event_loop()
loop.add_reader(sys.stdin, handle_stdin)
tasks = [tick(), print_hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()   
    
