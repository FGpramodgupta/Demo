from confluent_kafka import Consumer, KafkaException
from concurrent.futures import ThreadPoolExecutor
import threading
import sys

# Function to process each message
def process_message(msg):
    print(f"[{threading.current_thread().name}] Processing message: {msg.value().decode('utf-8')}")

def kafka_consumer_threaded():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest',  # Or 'latest' in production
        'enable.auto.commit': True
    }

    consumer = Consumer(conf)
    consumer.subscribe(['my-topic'])

    print("Kafka consumer started. Listening...")

    # Thread pool for processing messages concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            while True:
                msg = consumer.poll(timeout=1.0)  # Poll one message
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                # Submit the message to the thread pool
                executor.submit(process_message, msg)

        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            consumer.close()

if __name__ == "__main__":
    kafka_consumer_threaded()
