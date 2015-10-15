#http://makina-corpus.com/blog/metier/2015/python-http-server-with-the-new-async-await-syntax
import asyncio

@asyncio.coroutine
def slow_operation(n):
    yield from asyncio.sleep(1)
    print("Slow operation {} complete".format(n))


@asyncio.coroutine
def main():
    yield from asyncio.wait([
        slow_operation(1),
        slow_operation(2),
        slow_operation(3),
    ])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# As you can see, this example uses existing Python syntax: decorators and the yield keyword.

# Running this script gives us this output:

# $ python3.4 sleeping.py
# Slow operation 1 complete
# Slow operation 2 complete
# Slow operation 3 complete

# Now here is how the code may look like using the upcoming version 3.5 of Python:


async def slow_operation(n):
    await asyncio.sleep(1)
    print("Slow operation {} complete".format(n))


async def  main():
    await asyncio.wait([
        slow_operation(1),
        slow_operation(2),
        slow_operation(3),
    ])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
