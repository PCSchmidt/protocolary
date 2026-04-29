# EDC Adapter

This component integrates with downstream Electronic Data Capture (EDC) systems to transform study definitions into EDC-specific formats.

## Features

- Retrieval of study definitions from SDR
- Transformation to EDC-specific format
- Generation of form definitions
- Creation of edit checks

## Technology Stack

- .NET 6 or Node.js
- HTTP client for API communication
- Template engine for form generation

## Getting Started

1. Ensure .NET 6 SDK or Node.js is installed
2. Configure connection to SDR Core API in appsettings.json
3. Configure connection to EDC system in appsettings.json
4. Run the application using dotnet run or 
pm start

## Development

This component will be implemented as a new adapter for the POC.
