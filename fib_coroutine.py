"""Async fibonacci implementation taken from:
http://stackoverflow.com/questions/25105850/asyncio-with-mapreduce-flavor-and-without-flooding-the-event-loop"""     
import asyncio
import sys
from time import time
queue = asyncio.Queue()

def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data))

async def coro_sum(summands):
    return sum(summands)


async def fib(n):
    if n<=1:
        s = n
    else:
        await asyncio.sleep(0) #stops the computation from blocking 
        a = await fib(n-2) 
        b = await fib(n-1) 
        s = await coro_sum([a, b])
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
    
