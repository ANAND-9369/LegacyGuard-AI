import json
import time
from datetime import datetime
from typing import Dict, List, Any

class MonitoringAgent:
    """Multi-agent system for real-time monitoring and anomaly detection"""
    
    def __init__(self, agent_id: str, thresholds: Dict[str, float] = None):
        self.agent_id = agent_id
        self.thresholds = thresholds or {
            'low_threshold': 50,
            'high_threshold': 150,
            'variance_threshold': 20
        }
        self.anomalies_detected = []
        self.normal_readings = 0
        self.anomaly_readings = 0
        
    def analyze_sensor_data(self, sensor_reading: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze single sensor reading for anomalies"""
        analysis = {
            'sensor_id': sensor_reading.get('sensor_id'),
            'timestamp': datetime.now().isoformat(),
            'is_anomaly': False,
            'reason': '',
            'confidence': 0.0
        }
        
        value = sensor_reading.get('value', 0)
        
        # Check thresholds
        if value < self.thresholds['low_threshold']:
            analysis['is_anomaly'] = True
            analysis['reason'] = 'BELOW_LOW_THRESHOLD'
            analysis['confidence'] = 0.95
            self.anomaly_readings += 1
        elif value > self.thresholds['high_threshold']:
            analysis['is_anomaly'] = True
            analysis['reason'] = 'ABOVE_HIGH_THRESHOLD'
            analysis['confidence'] = 0.92
            self.anomaly_readings += 1
        else:
            analysis['is_anomaly'] = False
            analysis['reason'] = 'NORMAL_OPERATION'
            analysis['confidence'] = 0.98
            self.normal_readings += 1
        
        return analysis
    
    def batch_analyze(self, readings: List[Dict]) -> Dict[str, Any]:
        """Analyze batch of readings"""
        results = {
            'agent_id': self.agent_id,
            'batch_timestamp': datetime.now().isoformat(),
            'total_readings': len(readings),
            'analyses': []
        }
        
        for reading in readings:
            analysis = self.analyze_sensor_data(reading)
            results['analyses'].append(analysis)
            
            if analysis['is_anomaly']:
                self.anomalies_detected.append(analysis)
        
        results['anomalies_detected'] = len(self.anomalies_detected)
        results['normal_count'] = self.normal_readings
        results['anomaly_count'] = self.anomaly_readings
        
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get agent summary"""
        return {
            'agent_id': self.agent_id,
            'total_normal': self.normal_readings,
            'total_anomalies': self.anomaly_readings,
            'recent_anomalies': self.anomalies_detected[-5:]
        }

if __name__ == '__main__':
    agent = MonitoringAgent('agent_001')
    test_reading = {'sensor_id': 'sensor_0', 'value': 45}
    analysis = agent.analyze_sensor_data(test_reading)
    print(json.dumps(analysis, indent=2))
