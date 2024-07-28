import { Stack, StackProps, Duration } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Stream } from 'aws-cdk-lib/aws-kinesis';
import { Function, Runtime, Code, StartingPosition } from 'aws-cdk-lib/aws-lambda';
import { LambdaRestApi, LambdaIntegration } from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';
import {KinesisEventSource} from 'aws-cdk-lib/aws-lambda-event-sources';

export class IngestionStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create a Kinesis stream
    const stream = new Stream(this, 'WebhookEventsStream', {
      streamName: 'WebhookEvents',
      shardCount: 1,
      retentionPeriod: Duration.hours(24),
    })

    // Create a publisher lambda
    const publisherLambda = new Function(this, 'publisherLambda', {
      runtime: Runtime.PYTHON_3_10,
      code: Code.fromDockerBuild(path.join(__dirname, '../../assets/lambda/publisherLambda')),
      handler: 'index.handler',
      environment: {
        STREAM_NAME: stream.streamName,
      }
    });

    // Create a consumer lambda
    const consumerLambda = new Function(this, 'consumerLambda', {
      runtime: Runtime.PYTHON_3_10,
      code: Code.fromDockerBuild(path.join(__dirname, '../../assets/lambda/consumerLambda')),
      handler: 'index.handler',
      environment: {
        STREAM_NAME: stream.streamName,
      }
    });
    
    // Grant the Lambda function permissions to read and write to the Kinesis stream
    stream.grantWrite(publisherLambda);
    stream.grantRead(consumerLambda);

    // Create Event Source Mapping
    consumerLambda.addEventSource(new KinesisEventSource(stream, {
      batchSize: 100, // default
      startingPosition: StartingPosition.LATEST
    }));

    // Create an API Gateway REST API
    const api = new LambdaRestApi(this, 'WebhookEventsApi', {
      handler: publisherLambda,
      proxy: false,
    });

    // Integrate the Lambda function with the API Gateway
    const publisherIntegration = new LambdaIntegration(publisherLambda, {
      requestTemplates: {
        'application/json': JSON.stringify({
          // 'streamName': stream.streamName,
          'data': '$input.body',
        }),
      },
    });

    // Create a resource and method for the API Gateway
    const webhookEvents = api.root.addResource('webhook-events');
    webhookEvents.addMethod('POST', publisherIntegration);

  }
}
