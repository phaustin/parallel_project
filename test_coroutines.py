#http://blog.thumbtack.net/python-coroutines/
def coroutine(f):
    def wrapper(*arg, **kw):
        c = f(*arg, **kw)
        c.send(None)
        return c
    return wrapper

@coroutine
def logger(prefix="", next=None):
    while True:
        message = yield
        print("{0}: {1}".format(prefix, message))
        if next:
            next.send(message)

@coroutine
def cache_checker(cache, onsuccess=None, onfail=None):
    while True:
        request = yield
        if request in cache and onsuccess:
            onsuccess.send(cache[request])
        elif onfail:
            onfail.send(request)

@coroutine
def load_balancer(*workers):
    while True:
        for worker in workers:
            request = yield
            worker.send(request)

@coroutine
def worker(cache, response, next=None):
    while True:
        request = yield
        cache[request] = response
        if next:
            next.send(response)

cache = {}
response_logger = logger("Response")
cluster = load_balancer(
    logger("Worker 1", worker(cache, 1, response_logger)),
    logger("Worker 2", worker(cache, 2, response_logger)),
    logger("Worker 3", worker(cache, 3, response_logger)),
)
cluster = cache_checker(cache, response_logger, cluster)
cluster = logger("Request", cluster)

if __name__ == "__main__":
    from random import randint

    for i in range(20):
        cluster.send(randint(1, 5))
        
