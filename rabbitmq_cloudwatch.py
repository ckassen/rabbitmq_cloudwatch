import os
import requests
import urllib
from urlparse import urlparse
from boto.ec2.cloudwatch import *

class RabbitmqCloudwatchException(Exception):
    pass

def main():
    queues = os.getenv('RABBITMQ_CLOUWATCH_QUEUES', '').split(',')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION_NAME', 'us-west-1')

    cloudwatch_namespace = os.getenv(
        'RABBITMQ_CLOUWATCH_NAMESPACE', 'rabbitmq_cloudwatch')

    if not queues or not queues[0]:
        raise RabbitmqCloudwatchException('Queues may not be empty')

    broker_url = os.getenv('RABBITMQ_HTTP_URL')

    if not broker_url:
        raise RabbitmqCloudwatchException('Invalid URL')

    broker_url = urlparse(broker_url)

    if not all([
            broker_url.hostname, broker_url.username, broker_url.password]):
        raise RabbitmqCloudwatchException('Invalid URL')

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise RabbitmqCloudwatchException('Invalid AWS Credentials')

    cwc = connect_to_region(aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    for queue in queues:

        vhost, queue = queue.split('=')
        response = requests.get(broker_url.geturl() + urllib.quote_plus(vhost) + '/' + queue)

        if response.status_code == 200:
            queue_messages = response.json()['messages']

            print 'Queue {} on vhost {} currently has {} messages'.format(
                queue, vhost, queue_messages)

	    metric_name = vhost + '/' + queue
            cwc.put_metric_data(cloudwatch_namespace, metric_name, queue_messages)
        else:
            raise RabbitmqCloudwatchException(
                'Unable to fetch queue {} from url: {}. '
                'Error: {}={}'.format(
                    queue,
                    broker_url.geturl() + urllib.quote_plus(vhost) + '/' + queue,
                    response.status_code,
                    response.reason))

if __name__ == "__main__":
    main()
