#!/usr/bin/env python
import pika
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/hello', methods=['POST'])
def example():
    if request.is_json:
        data = request.get_json()  # Get the JSON data from the request
        message = data.get('message')  # Access the 'message' key in the JSON data
        # Process the message or perform any necessary operations
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ))
        print(" [x] Sent %r" % message)
        connection.close()

        response = {'status': 'success', 'message': f'Message received: {message}'}
        return jsonify(response)
    else:
        response = {'status': 'error', 'message': 'Invalid JSON'}
        return jsonify(response), 400

if __name__ == '__main__':
    app.run()
