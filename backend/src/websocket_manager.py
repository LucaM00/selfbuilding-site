import json
import asyncio
from typing import Dict, List, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from src.logging_config import agent_logger

class CreatorAgentMessenger:
    """WebSocket manager for creator-agent communication"""
    
    def __init__(self):
        # Store active WebSocket connections
        self.active_connections: List[WebSocket] = []
        
        # Command queue for orchestrator
        self.command_queue: asyncio.Queue = asyncio.Queue()
        
        # System state
        self.system_state = {
            "status": "active",
            "paused": False,
            "last_checkpoint": None,
            "current_task": None
        }
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        agent_logger.log_agent_action(
            agent="messenger",
            action="connection_established",
            level="info",
            message="Creator connected to WebSocket"
        )
        
        # Send current system state
        await self.send_to_connection(websocket, {
            "type": "system_state",
            "data": self.system_state,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
        agent_logger.log_agent_action(
            agent="messenger",
            action="connection_closed",
            level="info",
            message="Creator disconnected from WebSocket"
        )
    
    async def send_to_connection(self, websocket: WebSocket, message: dict):
        """Send message to a specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            agent_logger.log_agent_action(
                agent="messenger",
                action="send_error",
                level="error",
                message=f"Failed to send message: {str(e)}"
            )
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def handle_creator_command(self, websocket: WebSocket, message: dict):
        """Handle incoming commands from creator"""
        command_type = message.get("type")
        command_data = message.get("data", {})
        
        agent_logger.log_agent_action(
            agent="messenger",
            action="command_received",
            level="info",
            message=f"Received command: {command_type}",
            metadata={"command_data": command_data}
        )
        
        # Process different command types
        if command_type == "pause":
            await self.handle_pause_command()
        elif command_type == "resume":
            await self.handle_resume_command()
        elif command_type == "rollback":
            await self.handle_rollback_command(command_data.get("checkpoint"))
        elif command_type == "message":
            await self.handle_message_command(command_data.get("message", ""))
        elif command_type == "status":
            await self.send_to_connection(websocket, {
                "type": "system_state",
                "data": self.system_state,
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            await self.send_to_connection(websocket, {
                "type": "error",
                "message": f"Unknown command type: {command_type}",
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def handle_pause_command(self):
        """Handle system pause command"""
        self.system_state["paused"] = True
        self.system_state["status"] = "paused"
        
        # Add to command queue for orchestrator
        await self.command_queue.put({
            "type": "pause",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        agent_logger.log_agent_action(
            agent="orchestrator",
            action="system_paused",
            level="warning",
            message="System paused by creator command"
        )
        
        await self.broadcast({
            "type": "system_paused",
            "message": "System has been paused",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def handle_resume_command(self):
        """Handle system resume command"""
        self.system_state["paused"] = False
        self.system_state["status"] = "active"
        
        # Add to command queue for orchestrator
        await self.command_queue.put({
            "type": "resume",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        agent_logger.log_agent_action(
            agent="orchestrator",
            action="system_resumed",
            level="success",
            message="System resumed by creator command"
        )
        
        await self.broadcast({
            "type": "system_resumed",
            "message": "System has been resumed",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def handle_rollback_command(self, checkpoint: Optional[str]):
        """Handle rollback command"""
        if not checkpoint:
            await self.broadcast({
                "type": "error",
                "message": "Rollback command requires checkpoint parameter",
                "timestamp": datetime.utcnow().isoformat()
            })
            return
        
        # Add to command queue for orchestrator
        await self.command_queue.put({
            "type": "rollback",
            "checkpoint": checkpoint,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        agent_logger.log_agent_action(
            agent="orchestrator",
            action="rollback_requested",
            level="warning",
            message=f"Rollback to checkpoint requested: {checkpoint}"
        )
        
        await self.broadcast({
            "type": "rollback_initiated",
            "message": f"Rollback to checkpoint {checkpoint} initiated",
            "checkpoint": checkpoint,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def handle_message_command(self, message: str):
        """Handle general message command"""
        # Add to command queue for orchestrator
        await self.command_queue.put({
            "type": "message",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        agent_logger.log_agent_action(
            agent="orchestrator",
            action="creator_message",
            level="info",
            message=f"Creator message: {message}"
        )
        
        await self.broadcast({
            "type": "creator_message",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def get_next_command(self) -> Optional[dict]:
        """Get next command from queue (for orchestrator)"""
        try:
            return await asyncio.wait_for(self.command_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    def get_system_state(self) -> dict:
        """Get current system state"""
        return self.system_state.copy()

# Global messenger instance
messenger = CreatorAgentMessenger()

