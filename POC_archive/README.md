# TransCelerate DDF Commercial Adaptation POC

This directory contains the Proof of Concept (POC) implementation for the commercial adaptation of the TransCelerate Digital Data Flow (DDF) repositories.

## Overview

The POC demonstrates the technical feasibility and business value of adapting the DDF components for commercial use. It includes:

1. **SDR Core API** - A .NET 6 Web API that implements the core functionality of the Study Definition Repository
2. **StudyBuilder Adapter** - An adapter that integrates with upstream study design systems
3. **EDC Adapter** - An adapter that integrates with downstream Electronic Data Capture systems

## Prerequisites

- [.NET 6 SDK](https://dotnet.microsoft.com/download/dotnet/6.0)
- [Docker](https://www.docker.com/products/docker-desktop)
- [MongoDB](https://www.mongodb.com/try/download/community) (or use the Docker container)

## Project Structure

- /src - Source code for POC components
  - /SDR.Core.API - Core API implementation
  - /StudyBuilder.Adapter - Adapter for study design systems
  - /EDC.Adapter - Adapter for EDC systems
- /docs - Documentation and design artifacts
- /config - Configuration files
- /scripts - Setup and utility scripts
- /tests - Test cases and test data

## Getting Started

### Option 1: Running with Docker Compose

1. Make sure Docker is running
2. Open a terminal in the POC directory
3. Run the following command:

`ash
docker-compose up -d
`

This will start all components in Docker containers:
- MongoDB on port 27017
- SDR Core API on port 5000
- StudyBuilder Adapter
- EDC Adapter

### Option 2: Running Locally

1. Make sure MongoDB is running on localhost:27017
2. Open a terminal in the POC directory
3. Run the following commands:

`ash
# Run SDR Core API
cd src/SDR.Core.API
dotnet run

# In a new terminal, run StudyBuilder Adapter
cd src/StudyBuilder.Adapter
dotnet run

# In a new terminal, run EDC Adapter
cd src/EDC.Adapter
dotnet run
`

## Testing the POC

1. Access the SDR Core API Swagger UI at http://localhost:5000/swagger
2. Use the sample study definition in /tests/sample-study.json to create a new study
3. Verify the study is stored in MongoDB
4. Test the integration with the adapters

## Implementation Details

### SDR Core API

The SDR Core API provides endpoints for managing study definitions based on the USDM data model. It includes:

- CRUD operations for study definitions
- USDM data model implementation
- MongoDB integration for data storage
- Swagger documentation

### StudyBuilder Adapter

The StudyBuilder Adapter integrates with upstream study design systems to retrieve study design data and transform it to the USDM format for storage in the SDR.

### EDC Adapter

The EDC Adapter integrates with downstream Electronic Data Capture (EDC) systems to transform study definitions into EDC-specific formats.

## Next Steps

After validating the POC, the next steps would be:

1. Expand the implementation to include more features
2. Integrate with additional systems
3. Implement a comprehensive BiomedicalConcept library
4. Develop a production-ready deployment strategy

## Documentation

For more detailed information, see the following documents:

- [POC Strategy](../POC_STRATEGY.md)
- [Architecture Document](./docs/architecture.md)
