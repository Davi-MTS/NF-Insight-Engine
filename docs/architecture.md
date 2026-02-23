# System Architecture — FISCALIS

## 1. Architectural Overview

FISCALIS follows a layered pipeline architecture composed of three independent computational phases:

1. Data Acquisition Layer
2. Data Processing & Structuring Layer
3. Analytical Visualization Layer

The system is designed to ensure modular separation and deterministic data flow.

---

## 2. High-Level Architecture

```mermaid
flowchart LR
    A[Invoice Source] --> B[Phase 1: Ingestion]
    B --> C[Structured Extraction]
    C --> D[Phase 2: Data Structuring]
    D --> E[Database Storage]
    E --> F[Phase 3: Visualization & Analytics]
```

---

## 3. Layer Responsibilities

### Phase 1 — Ingestion
- QR Code / XML Reading
- Raw Data Parsing
- Key Extraction
- Initial Validation

### Phase 2 — Processing
- Web Scraping (Selenium)
- Structured Data Transformation
- Type Normalization
- Database Persistence

### Phase 3 — Visualization
- Data Aggregation
- Metric Computation
- Graphical Representation
- Analytical Dashboard Interface

---

## 4. Architectural Characteristics

- Layered separation
- Clear responsibility boundaries
- Expandable data flow
- Database-backed persistence
- Analytical-ready output
