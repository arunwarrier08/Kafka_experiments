from confluent_kafka import Producer
import json
from datetime import datetime
from ..config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

class MessageProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'value.serializer': lambda v: json.dumps(v).encode('utf-8')
        })
        self.topic = KAFKA_TOPIC

    def send_message(self, message: str):
        data = {
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        self.producer.produce(self.topic, value=data, callback=self.delivery_report)
        self.producer.flush()

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]") 