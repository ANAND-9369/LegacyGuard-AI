from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class AgentMemory:
    """Persistent memory for multi-agent communication and state tracking"""
    
    def __init__(self, max_memory_size: int = 1000, retention_hours: int = 24):
        self.events = deque(maxlen=max_memory_size)
        self.anomalies = deque(maxlen=max_memory_size)
        self.sop_recommendations = deque(maxlen=500)
        self.retention_hours = retention_hours
        self.created_at = datetime.now().isoformat()
        
    def add_event(self, event: Dict[str, Any]):
        """Add monitoring event to memory"""
        event['timestamp'] = datetime.now().isoformat()
        self.events.append(event)
        
    def add_anomaly(self, anomaly: Dict[str, Any]):
        """Add detected anomaly to memory"""
        anomaly['detected_at'] = datetime.now().isoformat()
        self.anomalies.append(anomaly)
        
    def add_sop(self, sop: Dict[str, Any]):
        """Add generated SOP recommendation"""
        sop['generated_at'] = datetime.now().isoformat()
        self.sop_recommendations.append(sop)
        
    def get_recent_anomalies(self, minutes: int = 30) -> List[Dict]:
        """Get anomalies from last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent = [a for a in self.anomalies 
                 if datetime.fromisoformat(a['detected_at']) > cutoff_time]
        return list(recent)
    
    def get_agent_state(self) -> Dict[str, Any]:
        """Get current agent memory state"""
        return {
            'created_at': self.created_at,
            'total_events': len(self.events),
            'total_anomalies': len(self.anomalies),
            'total_sops': len(self.sop_recommendations),
            'recent_anomalies': list(self.get_recent_anomalies(minutes=60)),
            'recent_events': list(list(self.events)[-10:])
        }
    
    def clear_old_data(self):
        """Clear data older than retention period"""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        # Note: deque doesn't support efficient filtering, so we rebuild
        new_events = deque(maxlen=self.events.maxlen)
        for event in self.events:
            if datetime.fromisoformat(event['timestamp']) > cutoff_time:
                new_events.append(event)
        self.events = new_events
        
    def export_memory(self) -> Dict[str, Any]:
        """Export memory for analysis or debugging"""
        return {
            'state': self.get_agent_state(),
            'events': list(self.events),
            'anomalies': list(self.anomalies),
            'sops': list(self.sop_recommendations)
        }

if __name__ == '__main__':
    memory = AgentMemory()
    memory.add_anomaly({'sensor_id': 'sensor_0', 'severity': 'HIGH'})
    print(json.dumps(memory.get_agent_state(), indent=2))
