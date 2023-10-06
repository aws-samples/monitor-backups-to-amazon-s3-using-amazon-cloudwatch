from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
import urllib.parse

metrics = Metrics(namespace="BackupsMonitoring") #the CloudWatch namespace: logical container to group all metrics for Backups

@metrics.log_metrics  # ensures metrics are flushed upon request completion/failure
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print("Start processing S3 Event")
    
    file_name = urllib.parse.unquote_plus(urllib.parse.unquote(event['Records'][0]['s3']['object']['key']))  #S3 event contains file name in URL encoding, needs to be decoded - https://github.com/aws-samples/amazon-textract-enhancer/issues/2
    print ("Backup file: " + file_name)
    
    system_name = file_name.split("/")[0] #the prefix of the file, i.e. the folder, which represents the system and the metric you want you monitor backups for
    system_name = file_name.split("/")[0] #the prefix of the file, i.e. the folder, which represents the system and the metric you want you monitor backups for
    metrics.add_metric(name=system_name, unit=MetricUnit.Count, value=1) #each time a backup file is copied to S3, push a custom metric with the name of folder as the system name, with the value of 1.
    print ("Pushed metric: " + file_name)