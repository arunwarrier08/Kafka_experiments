from src.producer.message_producer import MessageProducer
import json
from datetime import datetime

def test_send_message(mock_kafka_producer):
    # Create producer instance
    producer = MessageProducer()
    test_message = "Hello, World!"
    
    # Send test message
    producer.send_message(test_message)
    
    # Verify producer was called correctly
    mock_kafka_producer.produce.assert_called_once()
    
    # Get the args the mock was called with
    call_args = mock_kafka_producer.produce.call_args
    args = call_args[0]  # positional arguments
    kwargs = call_args[1]  # keyword arguments
    
    # Verify topic
    assert args[0] == producer.topic
    
    # Verify message format
    sent_data = json.loads(kwargs['value'].decode('utf-8'))
    assert sent_data['content'] == test_message
    assert 'timestamp' in sent_data
    
    # Verify flush was called
    mock_kafka_producer.flush.assert_called_once()

def test_delivery_report_success(mock_kafka_producer):
    producer = MessageProducer()
    mock_msg = type('Message', (), {
        'topic': lambda: 'test_topic',
        'partition': lambda: 0
    })
    producer.delivery_report(None, mock_msg)

def test_delivery_report_failure(mock_kafka_producer):
    producer = MessageProducer()
    mock_msg = type('Message', (), {
        'topic': lambda: 'test_topic',
        'partition': lambda: 0
    })
    test_error = "Test error"
    producer.delivery_report(test_error, mock_msg) 