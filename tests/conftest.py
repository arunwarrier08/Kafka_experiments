import pytest
from unittest.mock import MagicMock
from datetime import datetime

@pytest.fixture
def mock_db_connection(mocker):
    """Mock database connection fixture"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('src.consumer.message_consumer.psycopg2.connect', return_value=mock_conn)
    return mock_conn, mock_cursor

@pytest.fixture
def mock_kafka_producer(mocker):
    """Mock Kafka producer fixture"""
    mock_producer = MagicMock()
    mocker.patch('src.producer.message_producer.Producer', return_value=mock_producer)
    return mock_producer

@pytest.fixture
def mock_kafka_consumer(mocker):
    """Mock Kafka consumer fixture"""
    mock_consumer = MagicMock()
    mocker.patch('src.consumer.message_consumer.Consumer', return_value=mock_consumer)
    return mock_consumer 