import os

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fileListener import FileListener

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
    port = websocket.client.port
    print("new client from " +str(port) + " added to the file log " + str(filename))
    fileListener = FileListener(os.path.join(logfolder, filename + ".log"))
    try:
        while True:
            async for line in fileListener.listen():
                await websocket.send_text(line)
    except WebSocketDisconnect:
        websocket.close()
        print("client disconnected from the file " + str(filename))
        