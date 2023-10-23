from aws_lambda_powertools import Logger
import boto3
import os

MetricName = os.environ['MetricName']
BackupFrequencyPeriod = os.environ['BackupFrequencyPeriod']
CloudWatchMetricsNameSpace = os.environ['POWERTOOLS_METRICS_NAMESPACE']
DimensionName = os.environ['DimensionName']
SNSTopic = os.environ['SNSTopic']

logger = Logger()
client =  boto3.client('cloudwatch')


def create_metric_alarm(dimension_value):
    logger.info("Creating CloudWatch Alarm for: " + dimension_value)
    put_metric = client.put_metric_alarm(
                AlarmName=dimension_value,
                AlarmDescription="CloudWatch Alert: Backups to S3 has failed for " + dimension_value,
                MetricName=MetricName,
                Period=int(BackupFrequencyPeriod),
                Statistic='Sum',
                Namespace=CloudWatchMetricsNameSpace,
                Dimensions=[
                    {
                        'Name': DimensionName,
                        'Value': dimension_value
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
    logger.info("List available metrics and create CloudWatch alarms for each custom metric") 

    #TODO: check which alarms already exist before creating.
    #get the metrics that already exist
    list_metrics = client.list_metrics(
        Namespace=CloudWatchMetricsNameSpace,
        MetricName=MetricName
    )

    #iterate over list_metrics and find dimensions
    for metric in list_metrics['Metrics']:
        for dimensions in metric['Dimensions']:
            if dimensions["Name"] == DimensionName:
                dimension_value = (dimensions["Value"])
                #for each metric, create an alarm
                create_metric_alarm(dimension_value)

        