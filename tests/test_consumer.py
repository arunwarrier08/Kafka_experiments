from src.consumer.message_consumer import MessageConsumer
import json
from datetime import datetime

def test_consume_messages_success(mock_kafka_consumer, mock_db_connection, mocker):
    mock_conn, mock_cursor = mock_db_connection
    
    # Setup mock message
    test_data = {
        "content": "test message",
        "timestamp": datetime.now().isoformat()
    }
    mock_message = type('Message', (), {
        'value': lambda: json.dumps(test_data).encode('utf-8'),
        'error': lambda: None
    })
    
    # Set up the mock consumer behavior
    mock_kafka_consumer.poll.return_value = mock_message
    
    # Create consumer and patch its _should_continue method
    consumer = MessageConsumer()
    mocker.patch.object(consumer, '_should_continue', side_effect=[True, False])
    
    # Run the consumer
    consumer.consume_messages()
    
    # Verify database insertion with the exact query format from MessageConsumer._save_to_database
    expected_query = """
        INSERT INTO messages (message, timestamp)
        VALUES (%s, %s)
        """
    mock_cursor.execute.assert_called_with(expected_query, (test_data["content"], test_data["timestamp"]))
    mock_conn.commit.assert_called_once()

def test_consume_messages_error(mock_kafka_consumer, mock_db_connection, mocker):
    mock_conn, mock_cursor = mock_db_connection
    
    # Setup mock message with error
    mock_message = type('Message', (), {
        'error': lambda: "Kafka error",
        'value': lambda: None
    })
    
    # Set up the mock consumer behavior
    mock_kafka_consumer.poll.return_value = mock_message
    
    # Create consumer and patch its _should_continue method
    consumer = MessageConsumer()
    mocker.patch.object(consumer, '_should_continue', side_effect=[True, False])
    
    # Run the consumer
    consumer.consume_messages()
    print("This is a very long line that exceeds the maximum line length set by Flake8, which is typically 79 or 88 characters, and it should trigger a Flake8 error when you try to commit this file.")
    
    # Verify no database interaction occurred
    mock_cursor.execute.assert_not_called()
    mock_conn.commit.assert_not_called()

def test_consumer_cleanup(mock_kafka_consumer, mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    
    # Create consumer instance with mocked dependencies
    consumer = MessageConsumer()
    
    # Call close method
    consumer.close()
    
    # Verify all connections are closed
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_kafka_consumer.close.assert_called_once() 