---
phase: design
title: System Design & Architecture
description: Define the technical architecture, components, and data models
---

# 1. EFFECTIVE FEATURE DESIGN

## 1.1 Feature Definition
* **Noun (The Tool):** [What are we building?]
    * *Core Function:* [What does it do?]

## 1.2 Effectiveness Attributes
* **Sustainability Adjectives (Robustness):**
    * *Adjective:* [e.g., "Fault-Tolerant"]
    * *Implementation Strategy:* [e.g., "Use Try/Catch blocks and Retry logic"]

* **Efficiency Adjectives (Optimization):**
    * *Adjective:* [e.g., "Lightweight"]
    * *Implementation Strategy:* [e.g., "Minimize external dependencies"]

* **Scalability Adjectives (Volume):**
    * *Adjective:* [e.g., "Modular"]
    * *Implementation Strategy:* [e.g., "Decouple API logic from UI"]

## 1.3 Architecture & Data
**Visual Map:**
- Include a mermaid diagram:
  ```mermaid
  graph TD
    User --> Client[Client/Script]
    Client --> API[External Service/API]
    API --> Database[(Storage)]

Data Models:

[Define Inputs/Outputs]

[Define Schema if database is used]

1.4 RESOURCE IMPACT ANALYSIS (The "Price Tag")
This section must be completed before Approval.

Financial Impact (OpEx):

External Costs: [e.g., "Hosting: $X/mo", "API Fees: $Y/1k calls"]

Projected Monthly Run Rate: [$X.XX]

Build Cost (One-Time):

Time to Build: [Low/Medium/High]

Complexity Risk: [Low/Medium/High]

ROI Sanity Check:

Value Proposition: [Why is this worth the cost above?]

Alignment: [Does this fit the Founder's "Efficiency" constraint?]