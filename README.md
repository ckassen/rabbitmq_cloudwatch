# rabbitmq_cloudwatch
Basic python program for publishing rabbitmq queue lengths to Cloudwatch. This can be used to trigger autoscaling or monitors.

The following environment variables must be set:
* RABBITMQ_CLOUWATCH_QUEUES: comma separated list of queues to monitor
* RABBITMQ_HTTP_URL: The base http url for fetching queue details. ex: http://foo:bar@127.0.0.1:15672/api/queues/vhost/'
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
