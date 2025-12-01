import random
import json
from datetime import datetime, timedelta

class SensorSimulator:
    """Simulates pharmaceutical production line sensors"""
    
    def __init__(self, num_sensors=5):
        self.num_sensors = num_sensors
        self.baseline_values = {i: 100 + i*10 for i in range(num_sensors)}
        self.anomaly_threshold = 0.7
        
    def get_sensor_readings(self, timestamp=None):
        """Generate realistic sensor readings with occasional anomalies"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
            
        readings = {}
        for sensor_id in range(self.num_sensors):
            baseline = self.baseline_values[sensor_id]
            # Simulate normal operation with small variations
            normal_reading = baseline + random.uniform(-2, 2)
            
            # 30% chance of anomaly for demonstration
            if random.random() > self.anomaly_threshold:
                # Simulate anomaly (jam condition)
                anomaly_reading = baseline * random.uniform(0.4, 0.6)
                readings[f'sensor_{sensor_id}'] = {
                    'value': anomaly_reading,
                    'timestamp': timestamp,
                    'anomaly': True,
                    'severity': 'HIGH' if anomaly_reading < baseline * 0.5 else 'MEDIUM'
                }
            else:
                readings[f'sensor_{sensor_id}'] = {
                    'value': normal_reading,
                    'timestamp': timestamp,
                    'anomaly': False,
                    'severity': 'NORMAL'
                }
        
        return readings
    
    def batch_readings(self, num_batches=10, interval_seconds=2):
        """Generate a batch of readings with time intervals"""
        batches = []
        current_time = datetime.now()
        
        for i in range(num_batches):
            timestamp = (current_time + timedelta(seconds=i*interval_seconds)).isoformat()
            readings = self.get_sensor_readings(timestamp)
            batches.append({
                'batch_id': i,
                'readings': readings,
                'timestamp': timestamp
            })
        
        return batches

if __name__ == '__main__':
    simulator = SensorSimulator()
    # Generate sample readings
    readings = simulator.get_sensor_readings()
    print(json.dumps(readings, indent=2))
