import multiprocessing as mp
from multiprocessing import shared_memory
import time
import pickle
def processFunc (shm):
    while(True):
        data = pickle.loads(shm.buf[:])
        data["val"] = data["val"] + 1
        shm.buf[:] = pickle.dumps(data)
        time.sleep(1)

if __name__ == "__main__":
    # shm = mp.SharedMemory(name="my_shm")
    shm = shared_memory.SharedMemory(create=True, size=1024)
    shm.buf[:] = pickle.dumps({"val" : 1})

    p1 = mp.Process(target=processFunc, args=(shm,))
    p1.start()
    while(True):
        print("arr : ", pickle.loads(shm.buf[:]) )
        time.sleep(1)