# A.E.G.I.S.
**Autonomous Engine for Graph-based Interoperability & Synchronization**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Beta%20RC1-orange)]()
[![Protocol](https://img.shields.io/badge/Protocol-MCP%20%7C%20A2A-green)](https://modelcontextprotocol.io/)
[![Observability](https://img.shields.io/badge/Observability-OpenTelemetry-purple)](https://opentelemetry.io/)
[![License](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> **"Transforming Agent Orchestration: From Fragile Sequential Chains to Resilient CPM Graphs."**

---

##  Executive Summary

Current AI Agent architectures suffer from **cumulative latency** ($T_{total} = \sum T_{agents}$) and cascading fragility. Addressing the "Last Mile Production Gap," **A.E.G.I.S.** is a **Level 3 Collaborative Multi-Agent System** orchestrator that applies civil engineering principles to AI.

By utilizing the **Critical Path Method (CPM)**, A.E.G.I.S. models data dependencies to execute agents in parallel, reducing operational latency by up to **40%** while ensuring transactional integrity via **Fail-Fast** protocols and **Adaptive Capacity Control**.

---

##  System Architecture

A.E.G.I.S. implements a decoupled architecture aligned with modern Google Cloud AgentOps standards:

### 1. The CPM Engine (Orchestration Layer)
We abandon linear execution. The system dynamically calculates the **DAG (Directed Acyclic Graph)** of the operation.
* **Mathematical Parallelism:** Independent tasks are executed simultaneously.
* **Orchestration:** Centralized management of the "Think, Act, Observe" loop.



[Image of Critical Path Method CPM diagram]


### 2. Universal Interoperability
We solve the "$N \times M$" integration problem using open standards:
* ** Tools (MCP):** Standardized integration with external systems (Databases, APIs) using the *Model Context Protocol*.
* ** Collaboration (A2A):** Asynchronous task delegation between agents using the *Agent-to-Agent* protocol and dynamic discovery via *Agent Cards*.

### 3. Context Engineering
Advanced context window management to prevent reasoning degradation ("Context Rot"):
* **Session:** Ephemeral, compacted conversation history (Hot path).
* **Memory:** Long-term vector storage consolidated asynchronously.

---

##  Key Features (AgentOps)

| Feature | Technical Description | Business Impact |
| :--- | :--- | :--- |
| **Fail-Fast & Adaptive Timeouts** | Pre-flight "Health Checks" and dynamic P99-based timeouts. | **Zero Cost** on predictable failures. |
| **Observability** | Native instrumentation with **OpenTelemetry**. Structured Logs, Distributed Traces, and Metrics. | "Glass Box" debugging (vs Black Box). |
| **Continuous Evaluation** | Integrated **Agent Quality Flywheel**. Production failures feed the *Golden Dataset*. | Autonomous system improvement. |
| **Security** | Verifiable Agent Identity (SPIFFE) and *Least Privilege* policies. | Prevention of *Prompt Injection*. |

---

##  Performance Demo

*(View the full mathematical analysis in our [Simulation Notebook](./notebooks/monte_carlo_sim.ipynb))*

The following comparison demonstrates latency reduction in a "RFP Response" workflow simulated with 10,000 Monte Carlo iterations:

| Metric (P80) | Sequential Chain (Legacy) | A.E.G.I.S. (CPM Graph) | Improvement |
| :--- | :--- | :--- | :--- |
| **Total Latency** | 55 seconds | **32 seconds** | 🔻 **-41%** |
| **Success Rate** | 82% | **99%** (via Retry/Circuit Breaker) | 🛡️ **+17%** |

---

##  Installation & Usage

### Prerequisites
* Python 3.10+
* Docker (for local MCP servers)
* Google Cloud API Key (Vertex AI)

### Quick Start

1.  **Clone repository:**
    ```bash
    git clone [https://github.com/RobertoGPAI/aegis-core.git](https://github.com/RobertoGPAI/aegis-core.git)
    cd aegis-core
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Orchestrator (CLI Demo):**
    ```python
    # Run the interactive demo with Human-in-the-Loop gate
    python main.py "Generate Q4 Market Strategy"
    ```

---

##  Roadmap (Future Work)

* **Phase 2 (Self-Evolving):** Implementation of Level 4 agents capable of generating their own tools for novel tasks.
* **Phase 3 (Agent Gym):** Offline simulation environment for Reinforcement Learning.

---

##  References & Standards

Built following Google Cloud's reference architectures:
* *Introduction to Agents and Agent Architectures*
* *Prototype to Production: AgentOps*
* *Agent Tools & Interoperability with MCP*
* *Context Engineering: Sessions & Memory*

---

##  License

This project is licensed under **CC-BY-SA 4.0** (Creative Commons Attribution-ShareAlike 4.0 International), in compliance with the **Google Agents Intensive Hackathon** official rules.

You are free to:
* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
* **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
