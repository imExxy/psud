from app import app
from flask import Flask, render_template, redirect, url_for
import pika, sys

from app.models import Power


def sendmsg(task):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='powerImport', durable=True)


    channel.basic_publish(exchange='',
                          routing_key='powerImport',
                          body=str(task),
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    print(" [x] Sent ", task)

    connection.close()

@app.route("/")
@app.route("/index")
def index():
    power = Power.query.all()
    return render_template("tables.html", rows=power)

@app.route("/update")
def update():
    sendmsg("Push")
    return redirect(url_for('index'))