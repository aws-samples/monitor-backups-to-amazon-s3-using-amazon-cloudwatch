from aws_lambda_powertools import Logger
import boto3
import json
import os

SNSTopic = os.environ['SNSTopic']
CloudWatchMetricsNameSpace = os.environ['POWERTOOLS_METRICS_NAMESPACE']

MetricName = os.environ['MetricName']
DimensionName = os.environ['DimensionName']

logger = Logger()
client =  boto3.client('cloudwatch')


def create_metric_alarm(system):
    logger.info("Creating CloudWatch Alarm for: " + system)
    put_metric = client.put_metric_alarm(
                AlarmName=system,
                AlarmDescription=system + " Backups to S3",
                MetricName=MetricName,
                Period=86400,
                Statistic='Sum',
                Namespace=CloudWatchMetricsNameSpace,
                Dimensions=[
                    {
                        'Name': DimensionName,
                        'Value': system
                    },
                ],
                EvaluationPeriods=1,
                Threshold=1.0,
                ComparisonOperator='LessThanThreshold',
                AlarmActions=[SNSTopic],
                TreatMissingData='breaching'

    )
    logger.debug(put_metric) 

def lambda_handler(event, context):
    logger.info("Start creating CloudWatch alarms for each custom metric")

    list_metrics = client.list_metrics(
        Namespace='BackupsMonitoring',
        MetricName='Backups'
    )

    #iterate over list_metrics and find dimensions
    for metric in list_metrics['Metrics']:
        #print(metric['Dimensions'])
        for dimensions in metric['Dimensions']:
            #dimensions["Name"])
            if dimensions["Name"] == "System":
                system = (dimensions["Value"])
                
                create_metric_alarm(system)

        