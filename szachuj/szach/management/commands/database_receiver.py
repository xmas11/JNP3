import pika
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from szachuj.settings import MQ_NAME

class Command(BaseCommand):
    help = 'Waits for messages using rabitMQ'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
        database_channel = connection.channel()
        database_channel.queue_declare(queue=MQ_NAME)

        def callback(ch, method, properties, szachs):
                print " [x] Received %r" % (szachs,)
                for szach in serializers.deserialize('xml', szachs):
                    szach.save()

        database_channel.basic_consume(callback,
                                        queue=MQ_NAME,
                                        no_ack=True)
        print ' [*] Waiting for messages. To exit press CTRL+C'
        database_channel.start_consuming()

