from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import asyncio
from app.core.agent import run_intelligence_task

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {"agent": [], "mcp": [], "ports": []}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)
        await websocket.send_text(f"--- {channel.upper()} ONLINE ---")

    def disconnect(self, websocket: WebSocket, channel: str):
        if websocket in self.active_connections.get(channel, []):
            self.active_connections[channel].remove(websocket)

    async def broadcast(self, message: str, channel: str):
        for connection in self.active_connections.get(channel, []):
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/agent")
async def agent_v(request: Request): return templates.TemplateResponse("agent_view.html", {"request": request})

@app.get("/mcp")
async def mcp_v(request: Request): return templates.TemplateResponse("mcp_view.html", {"request": request})

@app.get("/ports")
async def ports_v(request: Request): return templates.TemplateResponse("port_view.html", {"request": request})

@app.get("/run_task")
async def run_task(command: str):
    # This background task prevents the browser from timing out
    asyncio.create_task(run_intelligence_task(command, manager))
    return {"status": "success"}

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)

    import os
import uvicorn

# This block ensures the app reads the port from Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
