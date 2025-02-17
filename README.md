# Kafka Python Demo

This project demonstrates the usage of Apache Kafka with Python, implementing a producer-consumer pattern and PostgreSQL integration. The application shows how to publish messages to Kafka topics and consume them while storing the data in PostgreSQL.

## Project Structure

```
kafka-python-demo/
├── src/
│ ├── consumer/
│ │ ├── message_consumer.py
│ ├── producer/
│ │ ├── message_producer.py
│ ├── config/
│ │ ├── settings.py
│ ├── __init__.py
│ ├── database/
│ │ ├── database.py
│ ├── requirements.txt
│ ├── docker/
│ │ ├── docker-compose.yml
│ ├── README.md

```
## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd kafka-python-demo
```

2. Create a Python virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Start the Docker containers:
```bash
cd docker
docker-compose up -d
```

5. Verify that all containers are running:
```bash
docker-compose ps
```

## Configuration

The application configuration is stored in `src/config/settings.py`. The default settings are:

- Kafka broker: localhost:9092
- Kafka topic: demo_topic
- PostgreSQL database: kafka_demo
- PostgreSQL user: kafka_user
- PostgreSQL password: kafka_password

You can modify these settings according to your needs.

## Usage

### Starting the Consumer

1. Open a terminal and activate your virtual environment
2. Run the consumer:
```bash
python -m src.consumer.message_consumer
```

The consumer will start listening for messages and store them in PostgreSQL.

### Publishing Messages

There are two ways to send messages:

1. Using send_test_message.py (Recommended):
```bash
# Send a single message
python send_test_message.py -m "Hello, Kafka!"

# Send multiple messages
python send_test_message.py -c 5

# Send messages with interval
python send_test_message.py -m "Periodic message" -c 3 -i 2
```

Options:
- `-m` or `--message`: Custom message to send (optional)
- `-c` or `--count`: Number of messages to send (default: 1)
- `-i` or `--interval`: Interval between messages in seconds (default: 0)

2. Using send_message.py (Simple single message):
```bash
python send_message.py
```

### Monitoring Kafka with Kafdrop

The project includes Kafdrop, a web UI for monitoring Kafka:

1. Access the Kafdrop UI:
```bash
http://localhost:9000
```

2. Features available in Kafdrop:
- View all topics and their configurations
- Monitor consumer groups and their offsets
- Browse messages in topics
- View broker information
- Check cluster health
- Create new topics
- View partition information

3. Common operations in Kafdrop:
- Click on a topic to view its details
- View messages: Select a topic → View Messages
- Check consumer groups: Click on "Consumer Groups"
- Monitor broker health: Click on "Brokers"

### Checking the Results

You can verify the messages are being stored in PostgreSQL by connecting to the database:

```bash
docker exec -it docker_postgres_1 psql -U kafka_user -d kafka_demo
```

Then query the messages table:
```sql
SELECT * FROM messages;
```

## Features

- **Message Producer**: Sends messages to Kafka topic with timestamps
- **Message Consumer**: Consumes messages and stores them in PostgreSQL
- **PostgreSQL Integration**: Automatic storage of messages with timestamps
- **Docker Setup**: Easy deployment with Docker Compose
- **Configurable**: Easy to modify settings through configuration file

## Error Handling

The consumer implements basic error handling:
- Graceful shutdown on interruption
- Database connection error handling
- Message processing error handling

## Development

To extend this project, you can:
1. Add more topics
2. Implement message validation
3. Add more complex processing logic
4. Implement retry mechanisms
5. Add logging and monitoring
6. Create additional consumers for different use cases

## Troubleshooting

1. If Kafka is not accessible:
   - Verify that the Docker containers are running
   - Check if the ports are correctly mapped
   - Ensure no other service is using port 9092

2. If PostgreSQL connection fails:
   - Verify PostgreSQL container is running
   - Check the database credentials in settings.py
   - Ensure port 5432 is available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
