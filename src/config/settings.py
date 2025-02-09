from dotenv import load_dotenv
load_dotenv()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "demo_topic"

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    "dbname": "kafka_demo",
    "user": "kafka_user",
    "password": "kafka_password",
    "host": "localhost",
    "port": "5432",
}
