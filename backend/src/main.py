import os
import sys
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.logging_config import agent_logger
from src.websocket_manager import messenger
from src.routes.user import router as user_router

app = FastAPI(title="Self-Building Site API", version="1.0.0")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_folder_path = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_folder_path):
    app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

# API routes
app.include_router(user_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Log system startup"""
    agent_logger.log_agent_action(
        agent="system",
        action="startup",
        level="success",
        message="Self-Building Site API started successfully"
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    agent_logger.log_agent_action(
        agent="system",
        action="health_check",
        level="info",
        message="Health check requested"
    )
    return {"status": "healthy", "message": "Self-Building Site API is running"}

@app.get("/api/status")
async def get_status():
    """Get system status"""
    agent_logger.log_agent_action(
        agent="orchestrator",
        action="status_check",
        level="info",
        message="System status requested"
    )
    
    system_state = messenger.get_system_state()
    
    return {
        "status": system_state["status"],
        "paused": system_state["paused"],
        "agents": {
            "orchestrator": "ready",
            "builder": "ready", 
            "tester": "ready",
            "critic": "ready"
        },
        "version": "1.0.0",
        "last_checkpoint": system_state["last_checkpoint"],
        "current_task": system_state["current_task"]
    }

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    """Get recent agent logs"""
    try:
        logs = agent_logger.get_recent_logs(limit)
        return {"logs": logs}
    except Exception as e:
        agent_logger.log_agent_action(
            agent="system",
            action="get_logs",
            level="error",
            message=f"Failed to retrieve logs: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Failed to retrieve logs")

@app.websocket("/ws/creator")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for creator-agent communication"""
    await messenger.connect(websocket)
    
    try:
        while True:
            # Receive message from creator
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                await messenger.handle_creator_command(websocket, message)
            except json.JSONDecodeError:
                await messenger.send_to_connection(websocket, {
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": agent_logger.logger.handlers[0].formatter.formatTime(
                        agent_logger.logger.makeRecord("", 0, "", 0, "", (), None)
                    )
                })
                
    except WebSocketDisconnect:
        messenger.disconnect(websocket)

@app.post("/api/creator/command")
async def creator_command_rest(command: dict):
    """REST fallback for creator commands"""
    agent_logger.log_agent_action(
        agent="messenger",
        action="rest_command",
        level="info",
        message=f"REST command received: {command.get('type', 'unknown')}"
    )
    
    # Simulate WebSocket message handling
    await messenger.handle_creator_command(None, command)
    
    return {"status": "command_processed", "command": command}

# Serve frontend files
@app.get("/{path:path}")
async def serve_frontend(path: str = ""):
    """Serve frontend files"""
    if not os.path.exists(static_folder_path):
        raise HTTPException(status_code=404, detail="Static folder not found")
    
    if path and os.path.exists(os.path.join(static_folder_path, path)):
        return FileResponse(os.path.join(static_folder_path, path))
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="index.html not found")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)

