# Versify Platform

**Status**: _Work-in-progress. Please create issues or pull requests if you have ideas for improvement._

The **Versify Platform** is a serverless backend for an NFT distribution platform. Functionalities are split across multiple micro-services that communicate either through asynchronous messages over [Amazon EventBridge](https://aws.amazon.com/eventbridge/) or over synchronous APIs.

<p align="center">
  <img src="docs/images/flow.png" alt="High-level flow across microservices"/>
</p>

## Getting started

To install the necessary tools and deploy this in your own AWS account, see the [getting started](docs/getting_started.md) guide in the documentation section.

## Architecture

### High-level architecture

This is a high-level view of how the different microservices interact with each other. Each service folder contains anarchitecture diagram with more details for that specific service.

<p align="center">
  <img src="docs/images/architecture.png" alt="High-level architecture diagram"/>
</p>

### Technologies used

**Communication/Messaging**:

- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) for service-to-service synchronous communication (request/response).
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/) for service-to-service asynchronous communication (emitting and reacting to events).

**Authentication/Authorization**:

- [Auth0](https://aws.amazon.com/cognito/) for managing and authenticating users, and providing JSON web tokens used by services.
- [API Keys](https://aws.amazon.com/iam/) for external service authorization
- [AWS Identity and Access Management](https://aws.amazon.com/iam/) for service-to-service authorization, either between microservices (e.g. authorize to call an Amazon API Gateway REST endpoint), or within a microservice (e.g. granting a Lambda function the permission to read from a DynamoDB table).

**Compute**:

- [AWS Lambda](https://aws.amazon.com/lambda/) as serverless compute either behind APIs or to react to asynchronous events.

**Storage**:

- [MongoDB](https://www.mongodb.com/) as a scalable NoSQL database for persisting informations.

**CI/CD**:

- [Serverless Framework](https://www.serverless.com/) for defining AWS resources as code in most services.

**Monitoring**:

- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) for metrics, dashboards, log aggregation.
- [AWS X-Ray](https://aws.amazon.com/xray/) for tracing across AWS services and across microservices.

### Backend services

| Services                | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| [account](account/)     | Account management for stores.                              |
| [analytics](analytics/) | Analytics service to run reports.                           |
| [chain](chain/)         | Blockchain management service.                              |
| [content](content/)     | Content management service.                                 |
| [order](order/)         | Order management system.                                    |
| [payment](payment/)     | Manages payment collection and refunds.                     |
| [product](product/)     | Source of truth for product information.                    |
| [user](user/)           | Provides user management, authentication and authorization. |

### Frontend services

| Services                     | Description                                 |
| ---------------------------- | ------------------------------------------- |
| [api](services/api-service/) | REST API for interacting with the services. |

### Infrastructure services

| Services        | Description                                          |
| --------------- | ---------------------------------------------------- |
| [event](event/) | Core event resources for deploying backend services. |

### Shared resources

| Name              | Description                                                                                                |
| ----------------- | ---------------------------------------------------------------------------------------------------------- |
| [docs](docs/)     | Documentation application for all services.                                                                |
| [shared](shared/) | Shared resources accessible for all services, such as common CloudFormation templates and OpenAPI schemas. |
| [tools](tools/)   | Tools used to build services.                                                                              |

## Documentation

See the [docs](docs/) folder for the documentation.

### Deployment Steps

1. Backup all data
1. Create/modify s3 buckets (cdn.versify vs cdn.dev.versifylabs.com)
1. Deploy Mongo Tables
1. Create Mongo Triggers
1. Deploy Mongo Search Indexes
1. Deploy services with `sls deploy`
1. Add API custom domain mapping
1. Add secrets to AWS Secrets Manager
1. Add parameters to AWS Secrets Manager
1. Add variables to Amplify app
1. Update Auth0 applications
1. Update Auth0 APIs
1. Update Auth0 roles
1. Update Auth0 actions
1. Update Stripe Webhook
1. Update Alchemy Webhook
1. Update Tatum Signature Endpoint on KMS
1. Deploy Amplify App

## Contributing

See the [contributing](CONTRIBUTING.md) and [getting started](docs/getting_started.md) documents to learn how to contribute to this project.
