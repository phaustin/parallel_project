#http://www.pythonsandbarracudas.com/blog/2015/12/3/asynchronous-constraint-of-memory-allocation
sem = asyncio.Semaphore(10)

async def process_video(filename):
    cap = cv2.VideoCapture(filename)
    tasks = list()
    frame_ind = 0
    while cap.isOpened():
        await sem.acquire()
        ret, frame = cap.read()
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
    sem.release()

    
