"""Async fibonacci implementation taken from:
http://stackoverflow.com/questions/25105850/asyncio-with-mapreduce-flavor-and-without-flooding-the-event-loop"""     
import logging,os
os.environ['PYTHONASYNCIODEBUG'] = '1'
import asyncio
logging.basicConfig(level=logging.DEBUG)
import sys
from time import time
from concurrent.futures import ProcessPoolExecutor
queue = asyncio.Queue()

def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data))


async def coro_sum(summands):
    return sum(summands)

@asyncio.coroutine
def fib34(n):
    if n<=1:
        s = n
    else:
        yield from asyncio.sleep(0) #stops the computation from blocking 
        a = yield from fib34(n-2) 
        b = yield from fib34(n-1) 
        s = yield from coro_sum([a, b])
    return s


async def fib35(n):
    if n<=1:
        s = n
    else:
        await asyncio.sleep(0) #stops the computation from blocking 
        a = await fib35(n-2) 
        b = await fib35(n-1) 
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

timed_fib34 = log_execution_time(fib34)               

timed_fib35 = log_execution_time(fib35)               

def tick():
    while True:
       text = yield from queue.get()
       n = int(text.strip())
       res = yield from timed_fib35(n)
       print('fib({}) = {}'.format(n, res))



async def print_hello():
    while True:
        print("{} - Hello world!".format(int(time())))
        await asyncio.sleep(3)    

import logging
loop = asyncio.get_event_loop()
numprocs=2
loop.set_default_executor(ProcessPoolExecutor(numprocs))
loop.add_reader(sys.stdin, handle_stdin)
tasks = [tick(), print_hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()   
    
