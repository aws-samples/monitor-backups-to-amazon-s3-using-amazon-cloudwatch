from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools import single_metric
from aws_lambda_powertools import Logger
import urllib.parse
import os

logger = Logger()
CloudWatchMetricsNameSpace = os.environ['POWERTOOLS_METRICS_NAMESPACE'] #the CloudWatch namespace: logical container to group all metrics for backups
metrics = Metrics(namespace=CloudWatchMetricsNameSpace) 

MetricName = os.environ['MetricName']
DimensionName = os.environ['DimensionName']

@metrics.log_metrics  # ensures metrics are flushed upon request completion/failure
def lambda_handler(event, context):
    logger.info("Start processing S3 Event")
    
    file_name = urllib.parse.unquote_plus(urllib.parse.unquote(event['Records'][0]['s3']['object']['key']))  #S3 event contains file name in URL encoding, needs to be decoded - https://github.com/aws-samples/amazon-textract-enhancer/issues/2
    logger.info("Backup file: " + file_name)
    
    system_name = file_name.split("/")[1] #the prefix of the file, i.e. the folder, which represents the system and the metric you want you monitor backups for
    #metrics.add_metric(name=MetricName, unit=MetricUnit.Count, value=1) #each time a backup file is copied to S3, push a custom metric with value of 1
    #metrics.add_dimension(name="System", value=system_name) #dimension as a key/value pair. Key: System, and Value: name of folder as the system name
    with single_metric(name=MetricName, unit=MetricUnit.Count, value=1) as metric:
        metric.add_dimension(name=DimensionName, value=system_name)
    logger.info("Pushed metric and dimension for: " + system_name)

