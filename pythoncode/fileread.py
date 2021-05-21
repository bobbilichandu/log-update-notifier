import time

with open("README.md") as f:
    for line in f:
        print(line)

# seek and tell are like pointers to this file
# we can go to a position in a file using seek
# we can get which position we are at in a file using tell
# how do pointer increment or decrement?
# well you can't go back, but you can front using f.readline()
# readline would move the pointer to next line

with open("README.md") as f:
    seek = 0
    where = -1
    while True: 
        f.seek(seek)
        line = f.readline()
        if line:
            print(line)
            where = f.tell()
            seek = where
        else:
            time.sleep(0.04)
        
