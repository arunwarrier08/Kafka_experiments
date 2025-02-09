from confluent_kafka import Consumer
import json
import psycopg2
import logging
from ..config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, POSTGRES_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MessageConsumer:
    def __init__(self):
        logger.info(
            f"Initializing consumer with bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}"
        )
        self.consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "group.id": "my_group",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
        )

        logger.info(f"Subscribing to topic: {KAFKA_TOPIC}")
        self.consumer.subscribe([KAFKA_TOPIC])

        logger.info("Connecting to PostgreSQL database...")
        self.db_conn = psycopg2.connect(**POSTGRES_CONFIG)
        self.cursor = self.db_conn.cursor()
        self._running = True
        logger.info("Consumer initialization complete")

    def _should_continue(self):
        return self._running

    def consume_messages(self):
        logger.info("Starting to consume messages...")
        try:
            while self._should_continue():
                message = self.consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    logger.error(f"Consumer error: {message.error()}")
                    continue

                data = json.loads(message.value().decode("utf-8"))
                logger.info(f"Received message: {data}")
                self._save_to_database(data)
                self._running = False

        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.close()

    def _save_to_database(self, data):
        query = """
        INSERT INTO messages (message, timestamp)
        VALUES (%s, %s)
        """
        self.cursor.execute(query, (data["content"], data["timestamp"]))
        self.db_conn.commit()
        logger.info(f"Saved message to database: {data}")

    def close(self):
        logger.info("Closing consumer connections...")
        self.cursor.close()
        self.db_conn.close()
        self.consumer.close()
        logger.info("Consumer shutdown complete")


def main():
    logger.info("Starting Kafka consumer application...")
    consumer = MessageConsumer()
    try:
        consumer.consume_messages()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        consumer.close()
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
