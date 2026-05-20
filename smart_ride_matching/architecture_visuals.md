# SafeHer Ride: System Architecture Visuals

This document contains the professional visual conversions of the SafeHer Ride system architecture. These are optimized for different presentation mediums while strictly preserving the underlying architecture logic.

## 1. Professional Visual Block Diagram (Presentation Ready)
*Optimized for PowerPoint, Keynote, and Project Presentations. Uses a clean, colorful layout to distinguish layers.*

```mermaid
graph TD
    classDef frontend fill:#2a1b42,stroke:#c084fc,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef aiEngine fill:#381a3d,stroke:#ec4899,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef coreEngine fill:#132a22,stroke:#10b981,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef database fill:#31220f,stroke:#f59e0b,stroke-width:2px,color:#fff,rx:10px,ry:10px;

    subgraph Front["📱 Frontend Layer (Streamlit)"]
        direction LR
        A[Book Ride UI]:::frontend
        B[Live Route Map UI]:::frontend
        C[Emergency SOS UI]:::frontend
        D[Driver Dashboard UI]:::frontend
    end

    subgraph AI["🧠 AI Intelligence Layer"]
        direction LR
        AI_Match[AI Safety Matching\n(Confidence & Risk)]:::aiEngine
        AI_Route[AI Route Intel\n(Safety & ETA)]:::aiEngine
        AI_SOS[AI SOS Escalation\n(Threat Assessment)]:::aiEngine
        AI_Dash[Booking Intel\n(Demand Positioning)]:::aiEngine
    end

    subgraph Core["⚙️ Core Operational Engines"]
        direction LR
        M_Engine[Matching Engine\n(Shortest Path)]:::coreEngine
        F_Engine[Fare Engine\n(Dynamic Pricing)]:::coreEngine
        R_Control[Ride Controller\n(Lifecycle)]:::coreEngine
        S_Manager[SOS Manager\n(Alerts)]:::coreEngine
    end

    subgraph DB["💾 Data Storage Layer"]
        direction LR
        DB_Drivers[(Drivers Database)]:::database
        DB_Riders[(Riders Database)]:::database
        DB_Bookings[(Bookings History)]:::database
    end

    %% High-level connections for structural visual
    Front --> AI
    AI --> Core
    Core --> DB
    
    %% Specific Action Flows
    A -.->|1. Request| AI_Match
    B -.->|Fetch Data| AI_Route
    C -.->|Trigger Alert| AI_SOS
    D -.->|Analytics| AI_Dash

    AI_Match -.->|2. Candidates| M_Engine
    AI_Match -.->|3. Pricing| F_Engine
    AI_Route -.->|Simulate| M_Engine
    B -.->|State| R_Control
    AI_SOS -.->|Assess Threat| S_Manager

    M_Engine -.->|Fetch| DB_Drivers
    R_Control -.->|Update| DB_Bookings
    S_Manager -.->|Update| DB_Bookings
    AI_Dash -.->|Analyze| DB_Bookings
```

## 2. Internship Report Diagram (Academic / Formal)
*Optimized for PDFs, documentation, and formal reports. Uses high-contrast grayscale patterns and left-to-right flow for readability.*

```mermaid
graph LR
    classDef presentation fill:#ffffff,stroke:#333333,stroke-width:1px,color:#000000;
    classDef aiService fill:#f5f5f5,stroke:#333333,stroke-width:2px,color:#000000,stroke-dasharray: 5 5;
    classDef business fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef persistence fill:#e8e8e8,stroke:#333333,stroke-width:1px,color:#000000;

    subgraph "1. Presentation Layer"
        A[Book Ride View]:::presentation
        B[Route Map View]:::presentation
        C[Emergency SOS]:::presentation
        D[Dashboard View]:::presentation
    end

    subgraph "2. AI Services Layer"
        AI1[AI Safety Matching]:::aiService
        AI2[AI Route Intelligence]:::aiService
        AI3[AI Emergency Escalate]:::aiService
        AI4[Booking Intelligence]:::aiService
    end

    subgraph "3. Business Logic Engines"
        C1[Matching Engine]:::business
        C2[Fare Engine]:::business
        C3[Ride Controller]:::business
        C4[SOS Manager]:::business
    end

    subgraph "4. Persistence Layer"
        D1[(Drivers Database)]:::persistence
        D2[(Riders Database)]:::persistence
        D3[(Bookings Database)]:::persistence
    end

    A --> AI1
    AI1 --> C1 & C2
    B --> AI2 & C3
    C --> AI3
    D --> AI4
    
    AI2 --> C1
    AI3 --> C4

    C1 --> D1
    C3 --> D3
    C4 --> D3
    AI4 --> D3
```

## 3. Clean Flowcharts by Layer

### A. Core Workflow (Book & Dispatch)
```mermaid
flowchart TD
    classDef start fill:#1e1e2e,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef process fill:#2d1b4e,stroke:#ec4899,stroke-width:2px,color:#fff;
    classDef core fill:#0f0a1a,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef data fill:#181825,stroke:#f59e0b,stroke-width:2px,color:#fff;

    User([Rider Requests Ride]):::start --> BookUI[Book Ride UI]:::start
    BookUI --> AI_Match{AI Safety Matching}:::process
    
    AI_Match -->|Calculate Risk| Fare[Fare Engine]:::core
    AI_Match -->|Find Safe Drivers| Match[Matching Engine]:::core
    
    Match --> DbDrivers[(Drivers DB)]:::data
    DbDrivers --> Return[Return Top Candidates]:::process
```

### B. Emergency SOS Architecture Flow
```mermaid
flowchart LR
    classDef alert fill:#3b0a0a,stroke:#ef4444,stroke-width:2px,color:#fff;
    classDef process fill:#2d1b4e,stroke:#ec4899,stroke-width:2px,color:#fff;
    classDef action fill:#0f0a1a,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef data fill:#181825,stroke:#f59e0b,stroke-width:2px,color:#fff;

    Trigger([Trigger SOS Alert]):::alert --> SOS_UI[Emergency SOS UI]:::alert
    SOS_UI --> AI_Threat{AI Threat Assessment}:::process
    
    AI_Threat -->|High Threat Level| SOS_Mgr[SOS Manager]:::action
    SOS_Mgr -->|Broadcast to Contacts| External[External APIs]:::action
    SOS_Mgr -->|Persist Audit Log| DB[(Bookings DB)]:::data
```
