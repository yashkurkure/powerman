from confluent_kafka import Consumer, KafkaError
import json

# Kafka configuration
conf = {
    'bootstrap.servers': 'head.testbed.schedulingpower.emulab.net:9092', 
    'group.id': 'python-consumer-1',
    'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
}

# Create the consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['pbsevents'])

# Consume messages in a loop
while True:
    msg = consumer.poll(1.0) 

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(f'Error:  {msg.error()}')
            break

    # Print the received message
    value = json.loads(msg.value())
    print(f'Received message: {value}')

# Close the consumer
consumer.close()