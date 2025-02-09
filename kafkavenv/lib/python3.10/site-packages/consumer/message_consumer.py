from confluent_kafka import Consumer
import json
import psycopg2
from ..config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, POSTGRES_CONFIG

class MessageConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True
        })
        self.consumer.subscribe([KAFKA_TOPIC])
        self.db_conn = psycopg2.connect(**POSTGRES_CONFIG)
        self.cursor = self.db_conn.cursor()

    def consume_messages(self):
        try:
            while True:
                message = self.consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    print(f"Consumer error: {message.error()}")
                    continue
                data = message.value()
                self._save_to_database(data)
        except Exception as e:
            print(f"Error consuming messages: {e}")
        finally:
            self.close()

    def _save_to_database(self, data):
        query = """
        INSERT INTO messages (message, timestamp)
        VALUES (%s, %s)
        """
        self.cursor.execute(query, (data['content'], data['timestamp']))
        self.db_conn.commit()

    def close(self):
        self.cursor.close()
        self.db_conn.close()
        self.consumer.close() 