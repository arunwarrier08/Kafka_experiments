from src.producer.message_producer import MessageProducer

producer = MessageProducer()
producer.send_message("Hello from Kafka Producer!") 