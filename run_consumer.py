from src.consumer.message_consumer import MessageConsumer
import signal
import sys
import time
import psycopg2
from src.config.settings import POSTGRES_CONFIG


def wait_for_postgres(max_retries=5, retry_interval=2):
    """Wait for PostgreSQL to be ready"""
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            conn.close()
            print("Successfully connected to PostgreSQL")
            return True
        except psycopg2.OperationalError:
            print(
                f"Waiting for PostgreSQL to be ready... (attempt {i+1}/{max_retries})"
            )
            time.sleep(retry_interval)
    return False


def signal_handler(sig, frame):
    print("\nShutting down consumer...")
    sys.exit(0)


def main():
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for PostgreSQL to be ready
    if not wait_for_postgres():
        print("Could not connect to PostgreSQL. Exiting...")
        sys.exit(1)

    print("Starting Kafka consumer...")
    consumer = MessageConsumer()

    try:
        consumer.consume_messages()
    except KeyboardInterrupt:
        print("\nShutting down consumer...")
    finally:
        consumer.close()
        print("Consumer shutdown complete")


if __name__ == "__main__":
    main()
