# Commercial Adaptation of TransCelerate DDF

## Overview

This repository contains a commercial adaptation project based on TransCelerate's Digital Data Flow (DDF) open-source components. As an independent developer, I am exploring the feasibility of adapting these components for commercial use, which is permitted under the Apache 2.0 license of the original repositories.

The TransCelerate DDF project provides a sustainable open-source Study Definition Repository (SDR) that serves as a foundation for standardizing and streamlining clinical trial data exchange. This commercial adaptation aims to build upon that foundation to create a viable product for pharmaceutical companies, CROs, and research institutions.

**Note**: This is not an official TransCelerate project. This is an independent commercial adaptation effort that leverages TransCelerate's open-source components.

## Original TransCelerate Components

This project builds upon the following TransCelerate DDF repositories:

- **ddf-directory** - Directory of DDF-compatible solutions from various vendors
- **ddf-home** - Documentation and website content for the DDF project
- **ddf-sdr-api** - .NET 6 Web API for the Study Definition Repository
- **ddf-sdr-platform** - Terraform Infrastructure as Code (IaC) for Azure deployment
- **ddf-sdr-support** - Support resources and documentation
- **ddf-sdr-ui** - Angular-based user interface for the SDR

## Key Components of the Commercial Adaptation

### Study Definition Repository (SDR)

The core of this commercial adaptation is the Study Definition Repository, which provides a standardized repository for storing and retrieving study definitions. The commercial adaptation enhances the original SDR with:

1. **Enhanced SDR Core API** - Building upon the original .NET 6 Web API with additional features for enterprise use
2. **Customized UI** - Extending the Angular-based UI with improved user experience and additional features
3. **Flexible Deployment** - Supporting various deployment options beyond Azure

### Unified Study Definitions Model (USDM)

The adaptation leverages the USDM data model for representing clinical study definitions, which includes:

- **StudyDefinition** - Top-level container for study information
- **ClinicalStudy** - Core study metadata
- **StudyDesign** - Study design details
- **BiomedicalConcept** - Standardized biomedical concepts
- **ScheduleTimeline** - Study timeline and activities

### Integration Framework

The commercial adaptation extends the integration capabilities with:

- **Enhanced StudyBuilder Adapter** - Improved integration with study design systems
- **Enhanced EDC Adapter** - Advanced integration with EDC systems
- **Additional System Adapters** - Support for a wider range of upstream and downstream systems

## Commercial Adaptation Strategy

### Commercial Product Vision

**Product Name**: StudyFlow (tentative)

**Product Description**: A comprehensive study definition management system that streamlines the process of designing clinical studies and implementing them in Electronic Data Capture (EDC) systems. The product leverages the TransCelerate DDF framework and USDM data model to provide a standardized approach to study design and implementation.

### Key Enhancements for Commercial Use

1. **Enhanced User Experience**
   - Improved UI for commercial users
   - Advanced visualization features
   - Customizable dashboards
   - Role-based access control

2. **Enterprise Features**
   - Multi-tenancy support for SaaS deployment
   - Advanced security features
   - Comprehensive audit trail
   - Performance optimizations for large-scale deployments

3. **Integration Ecosystem**
   - Pre-built adapters for popular systems
   - Adapter development kit for custom integrations
   - Validation and testing tools
   - Partner certification program

4. **Deployment Flexibility**
   - Cloud-based SaaS (Azure, AWS, GCP)
   - On-premises deployment
   - Hybrid deployment options
   - Containerized deployment

5. **Value-Added Services**
   - Reporting and analytics
   - BiomedicalConcept library management
   - Training and certification
   - Professional services for implementation

## Proof of Concept (POC)

The POC directory contains a proof of concept implementation for the commercial adaptation. It includes:

1. **SDR Core API** - A .NET 6 Web API that implements the core functionality of the Study Definition Repository
2. **StudyBuilder Adapter** - An adapter that integrates with upstream study design systems
3. **EDC Adapter** - An adapter that integrates with downstream Electronic Data Capture systems

### Current Status

The POC is currently in the early stages of development, with the following components in progress:

- **SDR Core API**: Basic implementation in place
- **StudyBuilder Adapter**: Initial structure only
- **EDC Adapter**: Initial structure only
- **BiomedicalConcepts**: Initial set defined

## Technical Architecture

### Core Components

1. **Study Definition Repository (SDR)**
   - Deploy core API components from TransCelerate repository with enhancements
   - Configure MongoDB/CosmosDB for data storage
   - Implement robust authentication and authorization
   - Support multiple USDM versions (1.9, 2.0, 3.0)

2. **System Adapters**
   - Enhanced adapter for study builder (upstream)
   - Enhanced adapter for EDC system (downstream)
   - Advanced transformation capabilities

3. **User Interface**
   - Enhanced Angular-based frontend
   - Improved study definition browser and editor
   - Advanced search and comparison features
   - Comprehensive administrative tools

### Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Backend API | .NET 6 | Matches TransCelerate implementation |
| Database | MongoDB/CosmosDB | Document storage for USDM JSON |
| Adapters | .NET 6 | Flexibility for system integration |
| Admin UI | Angular | Matches TransCelerate UI implementation |
| Metrics | Application Insights | Cloud-native monitoring |
| Deployment | Multiple options | Flexibility for different environments |

## Getting Started

### Prerequisites

- [.NET 6 SDK](https://dotnet.microsoft.com/download/dotnet/6.0)
- [Node.js](https://nodejs.org/) (for Angular UI)
- [Docker](https://www.docker.com/products/docker-desktop) (optional, for containerized deployment)
- [MongoDB](https://www.mongodb.com/) (or Azure Cosmos DB with MongoDB API)

### Setting Up the Development Environment

1. Clone this repository:
   `
   git clone https://github.com/yourusername/transcelerate-commercial-adaptation.git
   `

2. Navigate to the POC directory:
   `
   cd transcelerate-commercial-adaptation/POC
   `

3. Run the Docker Compose setup:
   `
   docker-compose up -d
   `

4. Access the SDR Core API at http://localhost:5000/swagger
5. Access the UI at http://localhost:4200

## Next Steps

The following steps are planned for the continued development of this commercial adaptation:

1. **Complete Core Components**
   - Implement authentication and authorization
   - Add data validation
   - Improve error handling
   - Set up metrics collection

2. **Implement Adapters**
   - Select systems for integration
   - Implement integration adapters
   - Develop transformations
   - Test with sample study designs

3. **End-to-End Testing**
   - Test full workflow from study design to EDC
   - Measure performance and accuracy
   - Document issues and solutions

4. **Evaluation and Documentation**
   - Analyze results against objectives
   - Document challenges and solutions
   - Refine technical architecture
   - Develop scaling strategy

## Licensing

This commercial adaptation is based on TransCelerate's DDF components, which are licensed under the Apache 2.0 license. The Apache 2.0 license allows for commercial use, modification, distribution, and sublicensing of the original code, provided that the license and copyright notices are included.

This commercial adaptation maintains the original Apache 2.0 license for all components derived from TransCelerate's repositories. Any new components developed specifically for this commercial adaptation may be subject to different licensing terms.

## Disclaimer

- This is an independent commercial adaptation of TransCelerate's DDF components and is not affiliated with or endorsed by TransCelerate Biopharma Inc.
- The original TransCelerate materials and information are provided AS IS. Any party using or relying on this information and these materials do so entirely at their own risk.
- This commercial adaptation may collect and store personal data (user credentials, email address, IP address) for authentication and audit log purposes. Users are responsible for compliance with any relevant privacy laws or regulations in any applicable jurisdiction.
- Any information put into the provided tools (including the UI or API) may be visible to all users, so it is recommended not to use commercially sensitive or confidential information.

## Windows Setup Guide for POC

You have all the necessary prerequisites installed except for MongoDB. Since you already have Docker installed, you can run MongoDB in a Docker container, which is the simplest approach.

### Running MongoDB with Docker

1. Open a command prompt and run the following command to start a MongoDB container:

`
docker run --name mongodb -d -p 27017:27017 mongo:latest
`

This will download the latest MongoDB image and start a container with the name 'mongodb', mapping port 27017 on your host to port 27017 in the container.

2. To verify that MongoDB is running, you can execute:

`
docker ps
`

You should see the MongoDB container in the list of running containers.

### Running the POC with Docker Compose

The POC directory contains a docker-compose.yml file that will set up all the necessary components, including:

- MongoDB
- SDR Core API
- StudyBuilder Adapter
- EDC Adapter

To run the entire POC using Docker Compose:

1. Navigate to the POC directory:
`
cd transcelerate/POC
`

2. Run Docker Compose:
`
docker-compose up -d
`

3. Access the SDR Core API at http://localhost:5000/swagger
4. Access the UI at http://localhost:4200

### Stopping the POC

When you're done, you can stop the containers:

`
docker-compose down
`

To stop just the MongoDB container (if you started it separately):

`
docker stop mongodb
docker rm mongodb
`

### Data Persistence

By default, the data in the MongoDB container will be lost when the container is removed. If you want to persist the data, you can add a volume mount to the docker run command:

`
docker run --name mongodb -d -p 27017:27017 -v mongodb_data:/data/db mongo:latest
`

This will create a Docker volume named 'mongodb_data' that will persist even if the container is removed.

## Summary

You're all set to run the TransCelerate DDF Commercial Adaptation POC on your Windows laptop! Here's a summary of your setup:

1. **Prerequisites Status**:
   -  .NET 6 SDK (version 6.0.136) - INSTALLED
   -  Node.js (version 18.17.0) - INSTALLED
   -  Docker (version 27.0.3) - INSTALLED
   -  MongoDB - NOT INSTALLED (but will use Docker instead)

2. **Recommended Approach**:
   - Use Docker Compose to run the entire POC, which will automatically set up MongoDB and all other components.
   - The docker-compose.yml file in the POC directory is already configured to use volume mounting for MongoDB data persistence.

3. **Next Steps**:
   - Navigate to the POC directory: cd transcelerate/POC
   - Run Docker Compose: docker-compose up -d
   - Access the SDR Core API at http://localhost:5000/swagger
   - Access the UI at http://localhost:4200

This approach leverages your existing Docker installation and provides the simplest path to getting the POC up and running on your Windows laptop.
