# SDR Core API

This component is the central API for the Study Definition Repository (SDR) in the POC implementation. It provides endpoints for managing study definitions based on the USDM data model.

## Features

- CRUD operations for study definitions
- USDM data model implementation
- Authentication and authorization
- Data validation and transformation

## Technology Stack

- .NET 6 Web API
- MongoDB for data storage
- Swagger for API documentation

## Getting Started

1. Ensure .NET 6 SDK is installed
2. Ensure MongoDB is running locally
3. Configure connection string in appsettings.json
4. Run the application using dotnet run

## API Endpoints

- GET /api/v3/studydefinitions/{studyId} - Get study definition by ID
- POST /api/v3/studydefinitions - Create new study definition
- PUT /api/v3/studydefinitions/{studyId} - Update study definition
- DELETE /api/v3/studydefinitions/{studyId} - Delete study definition

## Development

This component will be implemented by adapting the TransCelerate SDR API repository.
