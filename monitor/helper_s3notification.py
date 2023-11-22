from aws_lambda_powertools import Logger
import boto3
import os
from crhelper import CfnResource

helper = CfnResource()

MyBucket = os.environ['MyBucket']
CustomMetricsFunctionArn = os.environ['CustomMetricsFunctionArn']

logger = Logger()
client =  boto3.client('s3')


@helper.create
@helper.update
def CreateS3Notification(event, _):
    #s = int(event['ResourceProperties']['No1']) + int(event['ResourceProperties']['No2'])
    #helper.Data['Sum'] = s
    logger.info("Create S3 Bucket Event Notification to CustomMetricsFunction") 
    logger.info("CustomMetricsARN: " + CustomMetricsFunctionArn)
    logger.info("Bucket: " + MyBucket)

    response = client.put_bucket_notification_configuration(
        Bucket=MyBucket,
        NotificationConfiguration={
                'LambdaFunctionConfigurations': [
                    {
                        'Id': 'CustomMetricsFunction',
                        'LambdaFunctionArn': CustomMetricsFunctionArn,
                        'Events': [
                            's3:ObjectCreated:*',
                        ],
                    },
                ],
            },
    )
@helper.delete
def no_op(_, __):
    pass

def lambda_handler(event, context):
    helper(event, context)