from confluent_kafka import Producer
import json

# Kafka configuration
conf = {
    'bootstrap.servers': 'head.testbed.schedulingpower.emulab.net:9092',  # Adjust if your Kafka broker is elsewhere
    'client.id': 'pbs-hook-producer',
    'batch.num.messages': 1,  # Disable batching
}

# Create the producer instance
producer = Producer(conf)

# Sample JSON message
message = {
    'key': 'my_key',
    'value': 'Hello from Python producer!'
}

# Send the message
try:
    producer.produce('pbsevents', value=json.dumps(message))
    producer.flush()  # Ensure the message is sent immediately
    print('Message sent successfully')
except Exception as e:
    print(f'Error sending message: {e}')