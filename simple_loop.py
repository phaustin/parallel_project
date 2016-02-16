import asyncio
import urllib.parse
import sys
import pdb
import os

def fileCallback(*args):
    print("Received: " + sys.stdin.readline())

loop = asyncio.get_event_loop()
task = loop.add_reader(sys.stdin.fileno(), fileCallback)
loop.run_forever()
