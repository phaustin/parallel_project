#http://www.pythonsandbarracudas.com/blog/2015/12/3/asynchronous-constraint-of-memory-allocation

class AsyncAllocator(object):
    def __init__(self, max_size):
        self._max_size = max_size
        self._allocated_size = 0
        self._waiting_allocations = deque()

    async def allocate_data(self, size):
        if size > self.max_size:
            raise Exception('Requested size exceeds total allowed allocation size')
        if not self.can_allocate_now(size):
            logger.info("Can't allocate {} bytes right now, waiting for memory to be freed".format(size))
            future = asyncio.Future()
            self._waiting_allocations.append((future, size))
            await future
        self._allocated_size += size

    def deallocate_data(self, array):
        self._allocated_size -= array.nbytes
        new_deque = deque()
        for ind, (future, size) in enumerate(self._waiting_allocations):
            if self.can_allocate_now(size):
                future.set_result(0)
            else:
                new_deque.append((future, size))
        self._waiting_allocations = new_deque

    def can_allocate_now(self, size):
        return self._allocated_size + size <= self._max_size

#By plugging our video feed into the allocator, we can set a specific memory limit on tracked allocations without having to worry about explicitly throttling the processing of the video feed.

allocator = AsyncAllocator(2e9)
async def process_video(filename):
    cap = cv2.VideoCapture(filename)
    tasks = list()
    frame_ind = 0
    while cap.isOpened():
        ret, frame = cap.read()
        await allocator.allocate_data(frame.nbytes)
        if not ret:
            break
        tasks.append(asyncio.ensure_future(process_frame(frame, frame_ind)))
        frame_ind += 1
        await asyncio.sleep(0)
    await asyncio.gather(tasks)

async def process_frame(frame, frame_ind):
    logger.info("Processing frame {}".format(frame_ind))
    await asyncio.sleep(15.0)
    logger.info("Finished processing frame {}".format(frame_ind))
    allocator.deallocate_data(frame.nbytes)
    
