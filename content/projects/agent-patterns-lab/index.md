---
title: "Agent Patterns Lab"
description: "Practical design patterns, protocols, and architectures for building production multi-agent systems — from a single LangGraph pipeline to enterprise-grade, cloud-deployed agent architectures."
summary: "Nine design patterns for production multi-agent systems, with running code. From a single LangGraph pipeline to a cloud-deployed multi-team agent system using MCP and A2A."
date: 2026-04-10
weight: 20
draft: false
tags: ["agentic systems", "multi-agent", "A2A", "MCP", "LangGraph", "design patterns"]
categories: ["AI engineering"]
featureAlt: "Architecture diagram showing three agent teams communicating via A2A protocol across trust boundaries"
icon: "🤖"
showReadingTime: true
---

{{< lead >}}
The AI agent landscape today is where microservices were in 2014. Frameworks multiply weekly, but few teams have shipped production multi-agent systems. The gap is not tooling — it is architectural knowledge.
{{< /lead >}}

Agent Patterns Lab is a collection of **9 design patterns** that close that gap. Each pattern solves a named architectural problem with working code you can run, study, and adapt. The progression takes you from a single `POST /run` REST endpoint to a cloud-deployed, authenticated, dynamically-discoverable multi-agent system.

**Repository:** [github.com/ksopyla/agent-patterns-lab](https://github.com/ksopyla/agent-patterns-lab)

---

## Why This Project Exists

I have spent years building AI-powered products in enterprise environments. The recurring lesson: knowing *what* an agent framework can do is the easy part. Knowing *how to structure, deploy, and operate agents that work together* across services, trust boundaries, and cloud environments — that is the hard part, and almost nobody writes about it.

This project is my attempt to document the architectural decisions that matter, through code that actually runs. Every pattern:

- Solves a **real architectural problem** that the previous pattern cannot handle
- Has clear **"when to use / when to avoid"** criteria
- Shows **trade-offs**, not just happy paths
- Builds on the previous one — you experience the limitation before learning the solution

---

## The Design Patterns

### Foundation Tier — Single Docker network, one team, agent internals

| Pattern | Name | What It Solves | Key Concepts |
|---|---|---|---|
| 01 | Orchestrator Pipeline | Decomposing tasks across specialized agents | LangGraph StateGraph, tool use, LangSmith tracing |
| 02 | MCP Tool Integration | Standardized tool access for agents & AI clients | MCP servers/clients, Claude Code integration |
| 03 | Persistent Memory | Remembering across conversations | Checkpointer, PostgreSQL, thread management |
| 04 | Memory Lifecycle *(optional)* | Managing growing knowledge bases | Memory refiner, fact TTL, hierarchical memory |

### Distribution Tier — Multi-service, multi-team, real distributed systems

| Pattern | Name | What It Solves | Key Concepts |
|---|---|---|---|
| 05 | Distributed A2A | Cross-team agent communication | A2A protocol, Agent Cards, JSON-RPC |
| 06 | Async & Streaming | Non-blocking multi-team coordination | Async A2A, SSE streaming, parallel requests |
| 07 | Cross-Network Auth | Securing agents across trust boundaries | Auth0 OIDC, JWT, M2M tokens, zero-trust |

### Enterprise Tier — Production readiness, cloud deployment

| Pattern | Name | What It Solves | Key Concepts |
|---|---|---|---|
| 08 | Discovery & Observability | Finding agents and monitoring the system | Agent registry, OpenTelemetry, distributed tracing |
| 09 | Cloud Deployment | Production infrastructure on Azure | Container Apps, Bicep IaC, Managed Identity, CI/CD |

### Why Each Transition Matters

Every pattern exists because the previous one creates a real limitation:

```
P01 ─── Hardcoded tools can't be shared ──────────────── P02
P02 ─── Every request starts from scratch ────────────── P03
P03 ─┬─ Memory grows unbounded ──────────────────────── P04 (optional)
     └─ A second team arrives, can't import their code ─ P05
P05 ─── Third team needs both, sequential is too slow ── P06
P06 ─── Team 2 moves to external partner, no trust ──── P07
P07 ─── New agents appear, consumers need code changes ─ P08
P08 ─── Docker Compose doesn't work in production ───── P09
```

---

## The Domain: A Crypto Intelligence Platform

Abstract patterns are hard to internalize. Concrete stories stick. All nine patterns share a single, evolving domain — a crypto intelligence platform where three specialized teams emerge as complexity demands them.

```
 ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
 │  TEAM 1: INTELLIGENCE   │  │ TEAM 2: TECHNICAL       │  │ TEAM 3: TRADING         │
 │  (Patterns 01-04)       │  │ ANALYSIS (Pattern 05+)  │  │ SIGNALS (Pattern 06+)   │
 │                         │  │                         │  │                         │
 │  Research Planner       │  │  Price Collector        │  │  Signal Synthesizer     │
 │  News Scanner           │  │  Indicator Calculator   │  │  Risk Assessor          │
 │  Project Profiler       │  │  Level Analyst          │  │  Trade Advisor          │
 │  Community Analyst      │  │  Technical Reporter     │  │                         │
 │  Intelligence Compiler  │  │                         │  │                         │
 └────────────┬────────────┘  └────────────┬────────────┘  └────────────┬────────────┘
              │                            │                            │
              │         A2A Protocol       │         A2A Protocol       │
              └────────────────────────────┴────────────────────────────┘
```

The story unfolds in three acts:

**Act 1 — One Team, Growing Capabilities** (Patterns 01–04). You are Team 1: Intelligence. Three agents research crypto projects inside a single LangGraph pipeline. It works — until you hit hardcoded tools, stateless requests, and unbounded memory. Each limitation drives the next pattern.

**Act 2 — Teams Multiply, Protocols Emerge** (Patterns 05–06). Team 2: Technical Analysis arrives as a separate service with a separate codebase. You cannot `import` their code. You need a protocol. Then Team 3 needs data from both teams simultaneously — sequential calls take 50+ seconds. Async communication becomes the only viable path.

**Act 3 — Enterprise Reality** (Patterns 07–09). Team 2 moves to an external partner. Implicit trust is gone. New agents need dynamic discovery. Three teams deploy to Azure as independent Container Apps with Infrastructure as Code, Managed Identity, and per-team CI/CD pipelines.

---

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Language | Python 3.14+ / uv | Package and version management |
| Orchestration | LangGraph | Agent state graphs with typed state |
| Server | FastAPI | HTTP/protocol endpoints (REST → MCP → A2A) |
| Infrastructure | Docker Compose | Local multi-container environments |
| Observability | LangSmith | Tracing, debugging, performance monitoring |
| Tools | MCP | Standardized tool access (Pattern 02+) |
| Communication | A2A | Agent-to-agent protocol (Pattern 05+) |
| Authentication | Auth0 | OIDC-based M2M auth (Pattern 07+) |
| Cloud | Azure Container Apps | Production deployment (Pattern 09) |

---

## Quick Start

```bash
git clone https://github.com/ksopyla/agent-patterns-lab.git
cd agent-patterns-lab
cp .env.example .env
# Fill in your API keys (Azure OpenAI or Anthropic, LangSmith)

# Run Pattern 01 from inside the example folder
cd examples/01-orchestrator-pipeline
docker compose up --build

# Verify it's running
curl http://localhost:8000/health

# Submit a research request
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"input": "Research the Arbitrum crypto project"}'
```

Every pattern supports `VERBOSE=true` in `.env`, which logs agent reasoning steps, tool call inputs/outputs, inter-agent message payloads, and LangSmith trace IDs. Reading verbose output is how you learn what agents are actually doing.

---

## Project Structure

```
agent-patterns-lab/
├── examples/                  # One folder per pattern (self-contained)
│   ├── 01-orchestrator-pipeline/
│   │   ├── README.md          # Pattern documentation (theory + walkthrough)
│   │   ├── pyproject.toml
│   │   ├── docker-compose.yml
│   │   ├── endpoints.http     # Ready-to-run REST requests
│   │   ├── src/
│   │   └── tests/
│   └── ...
├── libs/common/               # Shared utilities (agent_common package)
├── docs/                      # Curriculum, vision, changelog
├── infra/                     # Docker base images, Azure Bicep templates
└── .github/                   # CI/CD workflows, PR templates
```

Each example is designed to run from inside its own folder. Examples share the repository-root `.env` file and the workspace `libs/common` package. Container images build from `infra/docker/base/Dockerfile.agent` with per-example build arguments.

---

## Open Source

The entire project is open source under the MIT license.

- **Code:** [github.com/ksopyla/agent-patterns-lab](https://github.com/ksopyla/agent-patterns-lab)
- **Blog:** [ai.ksopyla.com](https://ai.ksopyla.com)
