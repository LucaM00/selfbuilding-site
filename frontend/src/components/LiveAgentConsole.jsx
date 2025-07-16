import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Activity, Bot, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const LiveAgentConsole = () => {
  const [logs, setLogs] = useState([]);
  const [agentStatus, setAgentStatus] = useState({
    orchestrator: 'active',
    builder: 'idle',
    tester: 'idle',
    critic: 'idle'
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockLogs = [
      {
        id: 1,
        timestamp: new Date().toISOString(),
        agent: 'orchestrator',
        level: 'info',
        message: 'System initialized successfully',
        action: 'system_init'
      },
      {
        id: 2,
        timestamp: new Date(Date.now() - 30000).toISOString(),
        agent: 'orchestrator',
        level: 'info',
        message: 'Monitoring agent status',
        action: 'status_check'
      },
      {
        id: 3,
        timestamp: new Date(Date.now() - 60000).toISOString(),
        agent: 'builder',
        level: 'success',
        message: 'Frontend scaffold completed',
        action: 'scaffold_complete'
      },
      {
        id: 4,
        timestamp: new Date(Date.now() - 90000).toISOString(),
        agent: 'tester',
        level: 'info',
        message: 'Running health checks',
        action: 'health_check'
      }
    ];

    setLogs(mockLogs);

    // Simulate real-time updates
    const interval = setInterval(() => {
      const newLog = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        agent: ['orchestrator', 'builder', 'tester', 'critic'][Math.floor(Math.random() * 4)],
        level: ['info', 'success', 'warning'][Math.floor(Math.random() * 3)],
        message: [
          'Processing task queue',
          'Monitoring system health',
          'Checking for updates',
          'Validating configuration',
          'Optimizing performance'
        ][Math.floor(Math.random() * 5)],
        action: 'routine_task'
      };

      setLogs(prev => [newLog, ...prev.slice(0, 49)]); // Keep last 50 logs
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'idle':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'success':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            Agent Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(agentStatus).map(([agent, status]) => (
              <div key={agent} className="flex items-center gap-2 p-3 border rounded-lg">
                {getStatusIcon(status)}
                <div>
                  <div className="font-medium capitalize">{agent}</div>
                  <div className="text-sm text-gray-500 capitalize">{status}</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Live Activity Log
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-96">
            <div className="space-y-2">
              {logs.map((log) => (
                <div key={log.id} className="flex items-start gap-3 p-3 border rounded-lg">
                  <Badge variant="outline" className={getLevelColor(log.level)}>
                    {log.level}
                  </Badge>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <span className="font-medium capitalize">{log.agent}</span>
                      <span>•</span>
                      <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div className="mt-1 text-sm">{log.message}</div>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
};

export default LiveAgentConsole;

