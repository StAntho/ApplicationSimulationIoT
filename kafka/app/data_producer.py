from kafka import KafkaProducer
from time import sleep
import json
import random
from datetime import datetime

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_data():
    return {
        'sensor_id': random.randint(1, 4),
        'temperature': random.uniform(20.0, 30.0),
        'humidity': random.uniform(30.0, 60.0),
        'timestamp': datetime.utcnow().isoformat(),
        "distance": random.uniform(0.02, 0.25),
        "value": random.randint(1, 10),
        "heart_rate": random.randint(70, 225)
    }

while True:
    data = generate_data()
    producer.send('topic1', data)
    print("Sent data: {}".format(data))
    sleep(2)