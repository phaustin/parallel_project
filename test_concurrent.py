#http://stackoverflow.com/questions/16276423/pythons-concurrent-futures-iterate-on-futures-according-to-order-of-completi
import time
import concurrent.futures

x = [3, 1, 2]

def sleeper(secs):
    time.sleep(secs)
    print('I slept for {} seconds'.format(secs))
    return secs

# returns in the order given
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    print(list(executor.map(sleeper, x)))

# I slept for 1 seconds
# I slept for 2 seconds
# I slept for 3 seconds
# [3, 1, 2]

# returns in the order completed
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futs = [executor.submit(sleeper, secs) for secs in x]
    print([fut.result() for fut in concurrent.futures.as_completed(futs)])
    
