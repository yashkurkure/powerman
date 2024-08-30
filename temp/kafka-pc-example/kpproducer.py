from kafka import KafkaProducer
import json

# Kafka configuration
conf = {
    'bootstrap_servers': 'head.testbed.schedulingpower.emulab.net:9092', 
    'client_id': 'pbs-hook-producer',
}

# Create the producer instance
producer = KafkaProducer(
    bootstrap_servers=conf['bootstrap_servers'], 
    client_id=conf['client_id'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample JSON message
message = {
    'key': 'my_key',
    'value': 'Hello from Python producer!'
}

# Send the message
try:
    future = producer.send('pbsevents', value=message)  
    future.get(timeout=10)  # Block for up to 10 seconds for acknowledgement
    print('Message sent successfully')
except Exception as e:
    print(f'Error sending message: {e}')

# Close the producer when done
producer.close()