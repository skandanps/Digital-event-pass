
import pika
import logging
logging.getLogger("pika").setLevel(logging.ERROR)

def send_message_to_broker(user_id, routing_key, data):
    hostname = "localhost"

    # Create the connection parameters
    credentials = pika.PlainCredentials("guest", "guest")
    virtual_host = "/"
    parameters = pika.ConnectionParameters(host=hostname, port=5672, virtual_host=virtual_host, credentials=credentials)

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    if routing_key is None or routing_key == "":
        with connection.channel() as channel:
            channel.exchange_declare(exchange="public", exchange_type="fanout")
            channel.basic_publish(exchange="public", routing_key="", body=data)

    else:
        with connection.channel() as channel:
            channel.exchange_declare(exchange="user", exchange_type="direct")
            channel.basic_publish(exchange="user", routing_key=user_id, body=data)
    print("sent...")
    connection.close()
    return

if __name__ == "__main__":
    send_message_to_broker("1", "", "mav alert! Incoming storm, please be safe.")
    send_message_to_broker("1", "1", "Game night notification starting soon....")
