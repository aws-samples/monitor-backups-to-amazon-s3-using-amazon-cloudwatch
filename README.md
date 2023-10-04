## Build Amazon CloudWatch dashboards and alarms to monitor backups to Amazon S3

Amazon S3 offers industry-leading scalability and availability, and customers often use Amazon S3 as a backup target, for data from on-premise systems, including Linux or Windows servers. Usually, the AWS CLI is used in a script to copy these backups to Amazon S3. Customers may struggle to ensure that these backups are successful, and if they fail, to notify teams to resolve the issue.  Amazon S3 Event Notifications provides a mechanism for initiating events when backups land in an S3 bucket. 

In this pattern, we will create an Amazon S3 trigger to invoke a Lambda function that will publish a custom metric to Amazon CloudWatch, based on the backup data in S3. CloudWatch dashboards will allow you to monitor all backups in a single graph, and CloudWatch alarms will send notifications when backups fail, to help customers quickly resolve failing backups. 

This pattern uses AWS serverless services to implement an event-driven approach to monitor backup files in Amazon S3.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

