import pickle
import os
import threading
from time import sleep, time

import redis

redis_host = "localhost"
redis_port = 6379
redis_auth = ""

def push_updates_to_redis(filepath, key):
    r = redis.StrictRedis(redis_host, redis_port)
    try:
        f = open(filepath, "r")
        seek = 0
        while True:
            f.seek(seek)
            line = f.readline()
            seek = f.tell()
            if not line:
                break
    
        while True:
            f.seek(seek)
            line = f.readline()
            if line:
                value = {}
                value['time'] = time()
                value['log'] = line.strip()
                if line.strip():
                    r.set(key, pickle.dumps(value))
                    print(pickle.loads(r.get(key)))
                seek = f.tell()
            else:
                sleep(0.5)
    
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    logsfolder = "logfiles"
    threads = list()
    for filename in os.listdir(logsfolder):
        print("starting a thread for: ", filename)
        filepath = os.path.join(logsfolder, filename)
        print(filepath)
        x = threading.Thread(target=push_updates_to_redis, args=(filepath, filename,), daemon=True)
        threads.append(x)
        x.start()
        print(filename + "'s updates are being pushed to redis server running at port:" + str(redis_port))
    while True:
        pass
    
        
        