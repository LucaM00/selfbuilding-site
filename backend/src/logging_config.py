import logging
import os
import json
from datetime import datetime
from typing import Dict, Any

class AgentLogger:
    """Centralized logging system for all agents"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure main logger
        self.logger = logging.getLogger("selfbuilding_site")
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # File handler
        log_file = os.path.join(log_dir, "agents.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # JSON log file for structured logs
        self.json_log_file = os.path.join(log_dir, "structured_logs.jsonl")
    
    def log_agent_action(self, agent: str, action: str, level: str = "info", 
                        message: str = "", metadata: Dict[str, Any] = None):
        """Log an agent action with structured data"""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "action": action,
            "level": level,
            "message": message,
            "metadata": metadata or {}
        }
        
        # Log to console and file
        log_message = f"[{agent.upper()}] {action}: {message}"
        
        if level == "error":
            self.logger.error(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        elif level == "success":
            self.logger.info(f"✓ {log_message}")
        else:
            self.logger.info(log_message)
        
        # Write structured log
        with open(self.json_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_recent_logs(self, limit: int = 50) -> list:
        """Get recent structured logs"""
        logs = []
        
        if not os.path.exists(self.json_log_file):
            return logs
        
        try:
            with open(self.json_log_file, "r") as f:
                lines = f.readlines()
                
            # Get last N lines
            recent_lines = lines[-limit:] if len(lines) > limit else lines
            
            for line in reversed(recent_lines):
                try:
                    log_entry = json.loads(line.strip())
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error reading logs: {e}")
        
        return logs

# Global logger instance
agent_logger = AgentLogger()

