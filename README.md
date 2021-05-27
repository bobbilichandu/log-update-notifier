# log-update-notifier
A web application that send updates to the web application when a log file is updated


## How to run?

**Requirements:**

* *Operating System*: Ubuntu 18.04+
* *Python*: 3.8+
* *Python-pip*: 21.1.2+

## Setup the application

* Clone the repository
  
> git clone https://github.com/chandu1263/log-update-notifier.git

* Install python 3.8

> sudo apt-get install python3.8

[Or follow this article to install python3.8](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)

* Install python-pip

> sudo apt-get install python-pip

* Create a virtual environment with python3.8

> virtualenv --python=/usr/bin/python3.8 venv

This will create a virtual environment with python3.8 as default python

* Run the virtual environment
  
> source venv/bin/activate

* Now you are in the virtual environment.
  
> pip install --upgrade pip 

to get the latest version of pip

> pip install -r requirements.txt

To install all the dependencies

To run the code:

> uvicorn run:app --reload

Setup is Done, now let's dive into the code

### How to get updates of a file

You have a log file and you want to see the lines that are being added to that file in real time.

*How would you accomplish this?*

1. You run a infinite loop
2. And always keep checking if a new line is added to that log file
3. To keep checking if a new line a added, you need to maintain a pointer to the file and keep checking

[Pointers to a file, go through this article to find about seek and tell](https://www.geeksforgeeks.org/python-seek-function/)

> cd pythoncode

In this folder check the file [fileread.py](https://github.com/chandu1263/log-update-notifier/blob/main/pythoncode/fileread.py)

You can find how we can use seek and tell to get latest updates.

In this folder, you can see how a simple wsgi server is created to get the latest updates of a log file.

**How to run**

> python main.py webserver file.log
> python main.py tailserver file.log

First command creates a server with 127.0.0.1 as host and 8000 as port.
Second command connects a client to the server, you can check the log updates in real time at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Above code uses websockets and wsgi server, but it doesn't support multi client support. So let's see how can we create a multi client supported socket server.

### Multi Client support

> cd ../sockets

In this folder, [redis_dp.py](https://github.com/chandu1263/log-update-notifier/blob/main/sockets/redis_db.py) uses redis database server to get real time updates from the log files in the logs folder.

* Note: You need redis server to b installed on your system for this to work. Follow this [article](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04) to install redis on ubuntu 18.04

Once you run  
> python redis_db.py

Redis starts reading the files and updates the corresponding key value in the redis database for every new line that is updates
You can modify the logs folder by modifying the [line](https://github.com/chandu1263/log-update-notifier/blob/226da9ee5bf4f514414201ead2a2e8fe9d6629c3/sockets/redis_db.py#L42) here.

> python main.py

This starts your main server(which acts like a client to the redis server). Here in the code, you can see the, we restricted the server to let atmost 5 clients to be connected at any given time. You can modify the [line](https://github.com/chandu1263/log-update-notifier/blob/226da9ee5bf4f514414201ead2a2e8fe9d6629c3/sockets/main.py#L22) here.

Now you can open multiple terminals to connect to this server by opening multiple terminals and running the below command

> python clientSocket.py filename

You should replace the filename with the filename you want which is in logs folder.

*This architecture not only supports multiple clients but also supports multiple files in the logs folder. redis_db creates a thread for each log file*
*But if a new file is added to the log folder after you start running the redis code, redis won't keep track of the new files. Also, this creates a thread for each file even though it is not in out interest, due to this CPU load might be heavy*

### Fastapi websockets

> cd ..

Here you can see 2 files [run.py](https://github.com/chandu1263/log-update-notifier/blob/main/run.py) and [fileListener.py](https://github.com/chandu1263/log-update-notifier/blob/main/fileListener.py)

FileListener class in fileListener.py uses asyncio loop to check the file asynchronously if there are any updates.
once run you,
> uvicorn run:app --reload

web application starts running. You can open multiple webbrowser clients using the url http:127.0.0.1:8000/logdata/<filename_prefix>

filename_prefix is nothing but the prefix to ".log" in the filename

| Filename  | filename_prefix |
| --------  | --------------- |
| file1.log | file1           |
| file2.log | file2           |
| file3.txt | NOT SUPPORTED   |

Each client will create a websocket connection with the server and updates in the logs will be forwarded to all the corresponding clients.

**Resources & References**

1. [FastAPI websocket documentation](https://fastapi.tiangolo.com/advanced/websockets/)
2. [Tail server with wsgi and sockets](https://gist.github.com/mariocesar/7c4d825fe64957a51c6695e4b5176050)
3. [how to make FastAPI server completely async](https://github.com/tiangolo/fastapi/issues/3265)
    Above issue helped me figure on how to use async and await in FastAPI.
