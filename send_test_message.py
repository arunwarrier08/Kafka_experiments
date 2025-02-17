import argparse
from src.producer.message_producer import MessageProducer
import time


def send_messages(message=None, count=1, interval=0):
    """
    Send messages to Kafka topic
    Args:
        message (str): Message to send. If None, will send default test message
        count (int): Number of messages to send
        interval (float): Interval between messages in seconds
    """
    producer = MessageProducer()

    for i in range(count):
        msg = message or f"Test message {i+1} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        try:
            producer.send_message(msg)
            print(f"Sent message: {msg}")
            if interval and i < count - 1:  # Don't sleep after the last message
                time.sleep(interval)
        except Exception as e:
            print(f"Error sending message: {e}")


def main():
    parser = argparse.ArgumentParser(description="Send test messages to Kafka topic")
    parser.add_argument("-m", "--message", help="Message to send")
    parser.add_argument(
        "-c", "--count", type=int, default=1, help="Number of messages to send"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=0,
        help="Interval between messages in seconds",
    )

    args = parser.parse_args()
    send_messages(args.message, args.count, args.interval)


if __name__ == "__main__":
    main()
