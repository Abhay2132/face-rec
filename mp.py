import multiprocessing as mp
from multiprocessing import shared_memory
import time
import pickle
def processFunc ():
    shm = shared_memory.SharedMemory(name='a')
    while(True):
        data = pickle.loads(shm.buf[:])
        data["val"] = data["val"] + 1
        shm.buf[:] = pickle.dumps(data)
        time.sleep(1)

if __name__ == "__main__":
    # shm = mp.SharedMemory(name="a")
    shm = shared_memory.SharedMemory(name='a', create=True, size=1024)
    shm.buf[:] = pickle.dumps({"val" : 1})

    p1 = mp.Process(target=processFunc)
    p1.start()
    while(True):
        print("arr : ", pickle.loads(shm.buf[:]) )
        time.sleep(1)