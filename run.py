import os
from time import sleep
from typing import Optional

from fastapi import (Cookie, Depends, FastAPI, Form, Query, Request, WebSocket,
                     requests, status, templating, websockets)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logfolder = "logfiles"


@app.get("/logdata/{filename}")
async def getLogUpdates(request: Request, filename: str):
    return templates.TemplateResponse("main.html", context={"request": request, "filename": filename})

@app.websocket("/ws/{filename}")
async def websocket_endpoint(websocket: WebSocket, filename: str):
    await websocket.accept()
    filepath = os.path.join(logfolder, str(filename) + ".log")
    try:
        f = open(filepath, "r")
        seek = 0
        where = -1
        while True:
            f.seek(seek)
            line = f.readline()
            where = f.tell()
            seek = where    
            if not line:
                break
        while True:
            f.seek(seek)
            line = f.readline()
            if line:
                await websocket.send_text(line.strip())
                where = f.tell()
                seek = where
            else:
                sleep(0.5)
    finally:
        f.close()
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)