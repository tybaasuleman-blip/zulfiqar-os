import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import asyncio

# Ensure your folder structure has app/core/agent.py with this function
from app.core.agent import run_intelligence_task

app = FastAPI(title="Zulfiqar OS")

# Railway needs to know where your templates are
templates = Jinja2Templates(directory="app/templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "agent": [], 
            "mcp": [], 
            "ports": []
        }

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel in self.active_connections:
            self.active_connections[channel].append(websocket)
            await websocket.send_text(f"--- {channel.upper()} ONLINE ---")
        else:
            await websocket.close(code=1003)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.active_connections:
            if websocket in self.active_connections[channel]:
                self.active_connections[channel].remove(websocket)

    async def broadcast(self, message: str, channel: str):
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_text(message)
                except Exception:
                    # Connection might be closed
                    pass

manager = ConnectionManager()

# --- ROUTES ---

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "online", "system": "Zulfiqar OS"}

@app.get("/agent")
async def agent_v(request: Request): 
    return templates.TemplateResponse("agent_view.html", {"request": request})

@app.get("/mcp")
async def mcp_v(request: Request): 
    return templates.TemplateResponse("mcp_view.html", {"request": request})

@app.get("/ports")
async def ports_v(request: Request): 
    return templates.TemplateResponse("port_view.html", {"request": request})

@app.get("/run_task")
async def run_task(command: str):
    # This background task prevents the browser from timing out
    asyncio.create_task(run_intelligence_task(command, manager))
    return {"status": "task_initiated", "command": command}

# --- WEBSOCKET ---

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)
    try:
        while True:
            # This keeps the connection alive and waits for incoming data
            data = await websocket.receive_text()
            # If the client sends something, you can handle it here
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        print(f"Websocket Error: {e}")
        manager.disconnect(websocket, channel)

# This part is for local testing; Railway will use the 'Start Command' instead
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
