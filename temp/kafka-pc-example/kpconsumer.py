from kafka import KafkaConsumer
import json

# Kafka configuration
conf = {
    'bootstrap_servers': 'localhost:9092', 
    'group_id': 'python-consumer-1',
    'auto_offset_reset': 'earliest' 
}

# Create the consumer instance
consumer = KafkaConsumer(
    'pbsevents',
    bootstrap_servers=conf['bootstrap_servers'],
    group_id=conf['group_id'],
    auto_offset_reset=conf['auto_offset_reset'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Consume messages in a loop (no need to explicitly subscribe)
for msg in consumer:
    # Print the received message
    value = msg.value
    print(f'Received message: {value}')