# Agentomics

[![Langroid Status](https://img.shields.io/badge/Powered%20by-Langroid-orange)](https://github.com/langroid/langroid)
[![Build Status](https://github.com/akhilkarra/agentomics/actions/workflows/build.yml/badge.svg)](https://github.com/akhilkarra/agentomics/actions)
[![JupyterBook](https://img.shields.io/badge/JupyterBook-live-blue)](https://akhilkarra.github.io/agentomics/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![codecov](https://codecov.io/gh/akhilkarra/agentomics/branch/main/graph/badge.svg)](https://codecov.io/gh/akhilkarra/agentomics)

## Introduction

Welcome to **Agentomics**, a new framework for simulating macroeconomic dynamics using multi-agent systems powered by large language models (LLMs). This repository demonstrates how intelligent agents representing different financial institutions can interact dynamically to model and analyze economic behaviors under varying conditions.

### What is Agentomics?

Agentomics is a macroeconomic simulation framework that explores:

- How economic perturbations influence the behaviors of central and commercial banks.
- The magnitude of these perturbations and their impact on economic policy and lending behaviors.
- The predictive power of LLMs in simulating realistic agentic interactions and matching case studies.

This project leverages the LLM's trained knowledge to generate insights into economic decision-making processes, providing a practical tool for researchers and developers interested in AI-driven simulations of macroeconomic systems.

## Features

- **Multi-Agent Simulation**: Model interactions among Small Banks, Big Banks, and Central Banks in a realistic economic environment.
- **Powered by Langroid**: Utilize the `langroid` framework to create intelligent agents and manage their interactions.
- **Customizable Scenarios**: Easily introduce economic perturbations and analyze their effects on agent behavior.
- **Case Study Validation**: Evaluate how closely the simulation aligns with real-world economic case studies.

## Repository Setup

To set up the working environment:

1. Run the following command to install dependencies and set up an Anaconda virtual environment named `agentomics`:
   ```bash
   make env
   ```

2. Activate the virtual environment:
   ```bash
   conda activate agentomics
   ```

This will ensure all necessary packages are installed using the Poetry package manager, providing a ready-to-use environment for running simulations.

## Running the Simulation

The primary script for running the macroeconomic simulation is located at:

``scripts/economic_simulations/three_banks.py``

To execute the script:

```bash
python3 -m scripts.economic_simulations.three_banks
```

This simulation models interactions among three types of financial agents:

- **Small Banks**: Representing community-focused financial institutions.
- **Big Banks**: Representing large commercial banks with significant economic influence.
- **Central Banks**: Acting as regulatory authorities managing monetary policy.

The output provides insights into how economic perturbations and agent interactions influence the macroeconomic system.

## Learn More

For a detailed exploration of the project's architecture, features, and use cases, visit the accompanying [JupyterBook](https://akhilkarra.github.io/agentomics/) or read the blog post (coming soon!) that delves into the conceptual framework and implementation of Agentomics.

## Contributing

Contributions to Agentomics are welcome! Feel free to submit issues, feature requests, or pull requests to help improve the framework.
