import time
import logging

logging.basicConfig(filename='/var/log/myservice.log', level=logging.INFO)

def do_something():
    # Replace this with the core functionality of your service
    logging.info("Service is running")
    time.sleep(10)  # Simulate some work

if __name__ == '__main__':
    while True:
        do_something()