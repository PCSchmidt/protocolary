# POC Architecture Document

## Overview

This document outlines the architecture for the TransCelerate DDF Commercial Adaptation Proof of Concept (POC). The POC aims to validate the technical feasibility and business value of adapting the DDF components for commercial use.

## System Components

`
          
                                                             
  Study Builder    SDR Core API      EDC System    
   (Upstream)                                 (Downstream)   
                                                             
          
                               
                               
                               
                        
                                         
                           MongoDB DB    
                                         
                        
`

## Component Details

### 1. SDR Core API

- **Purpose**: Central component that manages study definitions
- **Technology**: .NET 6 Web API
- **Key Features**:
  - USDM data model implementation
  - RESTful API endpoints
  - Authentication and authorization
  - Data validation and transformation

### 2. Study Builder Adapter (Upstream)

- **Purpose**: Integrates with study design systems
- **Technology**: .NET 6 or Node.js
- **Key Features**:
  - Consumes study design data
  - Transforms to USDM format
  - Validates against USDM schema
  - Submits to SDR Core API

### 3. EDC Adapter (Downstream)

- **Purpose**: Integrates with EDC systems
- **Technology**: .NET 6 or Node.js
- **Key Features**:
  - Retrieves study definitions from SDR
  - Transforms to EDC-specific format
  - Generates form definitions
  - Creates edit checks

### 4. Database

- **Technology**: MongoDB
- **Key Features**:
  - Document storage for USDM JSON
  - Versioning support
  - Query capabilities

## Integration Patterns

### Study Builder to SDR

1. Study Builder creates/updates study design
2. Adapter retrieves study design data
3. Adapter transforms to USDM format
4. Adapter validates against USDM schema
5. Adapter submits to SDR Core API
6. SDR stores study definition in database

### SDR to EDC

1. EDC Adapter requests study definition from SDR
2. SDR retrieves study definition from database
3. EDC Adapter transforms to EDC-specific format
4. EDC Adapter generates form definitions
5. EDC Adapter creates edit checks
6. EDC Adapter submits to EDC system

## Authentication and Security

- Bearer token authentication
- Role-based authorization
- HTTPS for all communications
- Secure storage of credentials

## Deployment Architecture

For the POC, all components will be deployed locally:

- SDR Core API: Local development server
- Database: Local MongoDB instance
- Adapters: Local development servers

## Monitoring and Metrics

- Application logging
- Performance metrics collection
- Error tracking
- Business value metrics

## Next Steps

1. Set up development environment
2. Implement SDR Core API
3. Develop Study Builder Adapter
4. Develop EDC Adapter
5. Implement end-to-end workflow
6. Collect and analyze metrics
