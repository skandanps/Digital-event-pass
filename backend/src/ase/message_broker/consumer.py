import pika
import json

user_id = "1"
factory = pika.ConnectionParameters(host="localhost", port=5672, credentials=pika.PlainCredentials("guest", "guest"), virtual_host="/")
connection = pika.BlockingConnection(factory)
channel = connection.channel()
consumer_tag = "SimpleConsumer"
channel.exchange_declare(exchange="public", exchange_type="fanout")
channel.exchange_declare(exchange="user", exchange_type="direct")

queue_result = channel.queue_declare(queue="", durable=False, exclusive=True, auto_delete=True)
channel.queue_bind(exchange="public", queue=queue_result.method.queue)

channel.queue_declare(queue=user_id, durable=False, exclusive=True, auto_delete=True)
channel.queue_bind(exchange="user", queue=user_id, routing_key=user_id)

print(f"[{consumer_tag}] Waiting for messages...")

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"[{method.routing_key}] Received message: '{message}'")

channel.basic_consume(queue_result.method.queue, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=user_id, on_message_callback=callback, consumer_tag="userTag", auto_ack=True)


if __name__=="__main__":
    channel.start_consuming()
