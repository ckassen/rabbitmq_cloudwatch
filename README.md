# rabbitmq_cloudwatch
Basic python program for publishing rabbitmq queue lengths to Cloudwatch. This can be used to trigger autoscaling or monitors.

The following environment variables must be set:
* RABBITMQ_CLOUWATCH_QUEUES: comma separated list of vhost=queue pairs to monitor. The format is /vhost=queue, vhost must always start with a /.
* RABBITMQ_HTTP_URL: The base http url for fetching queue details, excluding vhost. ex: http://foo:bar@127.0.0.1:15672/api/queues/'
* RABBITMQ_CLOUWATCH_NAMESPACE: Namespace to publish metrics to
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
