# Main Agent App Architecture

# System Architecture

```

   ┌─────────────────┐
   │   User Input    │
   │ (PDF/JSON/Email)│
   └────────┬────────┘
            │
            ▼
┌─────────────────┐      ┌─────────────────┐
│ Classifier Agent├─────►│  Shared Memory  │
│                 │◄─────┤   (Redis/SQL)   │
└────────┬────────┘      └─────────────────┘
         │                        ▲
         ├──────────┬─────────────┤
         ▼          ▼             ▼
┌──────────────┐ ┌───────────┐ ┌──────────────┐
│ PDF Agent    │ │JSON Agent │ │Email Parser  │
│              │ │           │ │    Agent     │
└──────────────┘ └───────────┘ └──────────────┘
         │          │             │
         └──────────┴─────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │ Structured Output│
         │   (API)          │
         └──────────────────┘

```

# Overview

- **User Input**: Accepts PDF, JSON, or Email data.
- **Classifier Agent**: Determines the type of input and routes it to the appropriate agent.
- **Shared Memory (Redis/SQL)**: Central storage for sharing data between agents.
- **PDF Agent / JSON Agent / Email Parser Agent**: Specialized agents for processing each input type.
- **Structured Output (CRM/API)**: Final structured data output for downstream systems.


