# SafeHer Ride: AI-Powered Women Safety Platform

This document outlines the high-level architecture and system flow of the **SafeHer Ride** platform.

## System Flow Diagram

The following Mermaid diagram illustrates the interaction between the frontend pages, the AI safety engines, and the core operational backend modules.

```mermaid
graph TD
    %% Define styles
    classDef frontend fill:#1e1e2e,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef aiEngine fill:#2d1b4e,stroke:#ec4899,stroke-width:2px,color:#fff;
    classDef coreEngine fill:#0f0a1a,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef database fill:#181825,stroke:#f59e0b,stroke-width:2px,color:#fff;

    subgraph "Frontend Layer (Streamlit Pages)"
        A[Book Ride UI]:::frontend
        B[Live Route Map UI]:::frontend
        C[Emergency SOS UI]:::frontend
        D[Driver Dashboard UI]:::frontend
    end

    subgraph "AI Intelligence Layer"
        AI_Match[AI Safety Matching Engine\n(Confidence & Risk Level)]:::aiEngine
        AI_Route[AI Route Intelligence\n(Safety Analysis & ETA)]:::aiEngine
        AI_SOS[AI Emergency Escalation\n(Threat Level Assessment)]:::aiEngine
        AI_Dash[Booking Intelligence\n(Demand & Optimal Positioning)]:::aiEngine
    end

    subgraph "Core Operational Engines"
        M_Engine[Matching Engine\n(Shortest Path & Ranking)]:::coreEngine
        F_Engine[Fare Engine\n(Dynamic Pricing)]:::coreEngine
        R_Control[Ride Controller\n(Ride Lifecycle)]:::coreEngine
        S_Manager[SOS Manager\n(Alerts & Notifications)]:::coreEngine
    end

    subgraph "Data Storage"
        DB_Drivers[(Drivers Database)]:::database
        DB_Riders[(Riders Database)]:::database
        DB_Bookings[(Bookings History)]:::database
    end

    %% Flow - Book Ride
    A -->|1. Request Ride| AI_Match
    AI_Match -->|2. Get Candidates| M_Engine
    M_Engine -->|3. Fetch Drivers| DB_Drivers
    AI_Match -->|4. Get Fare| F_Engine
    
    %% Flow - Route Map
    B -->|Fetch Live Data| AI_Route
    AI_Route -->|Simulate Path| M_Engine
    B -->|Manage State| R_Control
    R_Control -->|Update DB| DB_Bookings

    %% Flow - SOS
    C -->|Trigger Alert| AI_SOS
    AI_SOS -->|Assess Threat| S_Manager
    S_Manager -->|Update DB| DB_Bookings
    
    %% Flow - Driver Dashboard
    D -->|Fetch Analytics| AI_Dash
    AI_Dash -->|Analyze Data| DB_Bookings
```

## Module Responsibilities

1. **AI Intelligence Layer** (`algorithms/ai_engine.py`): Serves as the central brain, exposing clear interfaces for match confidence, live route threat analysis, and automated emergency escalation.
2. **Core Matching Engine** (`algorithms/matching_engine.py`): Performs heavy-lifting graph traversal (Dijkstra's algorithm) to physically rank nearest available verified drivers.
3. **Fare Engine** (`algorithms/fare_engine.py`): Dynamically calculates cost based on safety prioritization and distance.
4. **SOS Manager** (`algorithms/sos_manager.py`): Interacts directly with communication APIs (simulated) to ensure highest-priority data sharing with emergency contacts.
