# Agentomics

[![Langroid Status](https://img.shields.io/badge/Powered%20by-Langroid-orange)](https://github.com/langroid/langroid)
[![Build Status](https://github.com/akhilkarra/agentomics/actions/workflows/build.yml/badge.svg)](https://github.com/akhilkarra/agentomics/actions)
[![JupyterBook](https://img.shields.io/badge/JupyterBook-live-blue)](https://akhilkarra.github.io/agentomics/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

## Introduction

Welcome to Agentomics! A repository for creating a macroeconomic simulation powered by a multi-agent LLM system.

The specific goal of this simulation is to see how introducing pertubations in different economic metrics could influence the behaviors of central and commercial banks, and how different magnitudes of such pertubations can influence major changes in economic policy and lending behaviors. I aim to achieve this using the information stored in the LLM's weights after training, and in doing so, evaluating how closely the LLM's predictions match different existing case studies to evaluate its validity (even if these are not necessarily out-of-sample evaluations).

This repository contains a script for this economic simulation and associated custom modules and utilities.

## Repository Setup

To set up the working environment in your workspace, run ``make env``. This will create an Anaconda virtual environment named "agentomics" and will install all the necessary packages using the Poetry package manager. After installation, run ``conda activate agentomics`` to activate the environment.

## Running Experiment

The main experiment script is stored under ``scripts/economic_simulations/three_banks.py``. To run this experiment, execute the command
``python3 -m scripts/economic_simulations/three_banks/py`` at the root of the repository.
