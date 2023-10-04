from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
import urllib.parse

metrics = Metrics(namespace="BackupsMonitoring")

@metrics.log_metrics  # ensures metrics are flushed upon request completion/failure
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print("Start processing S3 Event")
    
    filename = urllib.parse.unquote_plus(urllib.parse.unquote(event['Records'][0]['s3']['object']['key']))  #S3 event contains document name in URL encoding, needs to be decoded - https://github.com/aws-samples/amazon-textract-enhancer/issues/2
    print ("Customer Backup: " + filename)
    
    customer_name = filename.split("/")[0] #the prefix, i.e. the folder, is the customer name
    metrics.add_metric(name=customer_name, unit=MetricUnit.Count, value=1)