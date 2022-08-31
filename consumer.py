import time
import random

import requests
import pika

from models import Order


ORDER_CREATED = 'orderCreated'


def on_order_created(ch, method, properties, body):
    order = Order.parse_raw(body)
    # Comunicacao com o cartao de credito
    time.sleep(10)

    success = random.random() > 0.5

    if success:
        message = {"status": "approved"}
        print(f'Sucesso na ordem {order.order_id}')
    else:
        message = {"status": "cancelled"}
        print(f'Falha na ordem {order.order_id}')

    # PUT para o Order
    resp = requests.put(
        url=f'http://localhost:8000/order/{order.order_id}/status',
        json=message
    )
    print(resp)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=ORDER_CREATED)

    channel.basic_consume(
        queue=ORDER_CREATED,
        on_message_callback=on_order_created,
        auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    main()
