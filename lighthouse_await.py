#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#http://lighthouseinthesky.blogspot.ca/2015/10/numerical-coroutines.html

import concurrent.futures
import asyncio
import time
import numpy as np

async def pmap(f, xs, loop=None):
    fs = [asyncio.ensure_future(f(*x), loop=loop) for x in xs]
    await asyncio.wait(fs)
    return [f.result() for f in fs]

class Integrator:
    def __init__(self, f, cores=None):
        self.f = f
        self.loop = asyncio.get_event_loop()
        self.pool = concurrent.futures.ProcessPoolExecutor(cores)
        # This cache stores coroutines (partially or fully completed
        # calculations of f(x)). If you want a value, wait for the
        # coroutine to finish (it may have already) and then take
        # its result.
        self._f_cache = {}

    def integrate_interval(self, a, b, atol=1e-10):
        return self.loop.run_until_complete(
            self._integrate_interval(a, b, atol))

    async def _f(self, x):
        if x not in self._f_cache:
            self._f_cache[x] = self.loop.run_in_executor(self.pool, self.f, x)
        return (await asyncio.wait_for(self._f_cache[x],
                                            timeout=None, loop=self.loop))


    async def _simpson(self, a, b):
        c = (a+b)/2
        h3 = np.abs(b-a)/6
        fa, fb, fc = await pmap(self._f, [(a,), (b,), (c,)])
        return h3*(fa+4*fc+fb)

    async def _integrate_interval(self, a, b, atol):
        c = (a+b)/2
        sl, sa, sr = await pmap(self._simpson, [(a,c), (a,b), (c,b)])
        if np.abs(sl+sr-sa)<=15*atol:
            return sl + sr + (sl+sr-sa)/15
        else:
            rl, rr = await pmap(self._integrate_interval, [(a,c,atol/2),
                                                                (c,b,atol/2)])
            return rl+rr


if __name__=='__main__':
    def f(x):
        time.sleep(0.1)
        #print(x)
        return np.sin(x)

    now = time.time()
    I = Integrator(f, cores=16)
    r = I.integrate_interval(0, np.pi)
    print(r,len(I._f_cache),time.time()-now)
    
