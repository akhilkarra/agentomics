# Agentomics

## Introduction

Welcome to Agentomics! A repository for economic simulations powered by multi-agent LLM systems. This repository contains scripts for some economic simulations and associated custom modules and utilities.

## Repository Setup

To set up the working environment in your workspace, run ``make env``. This will create an Anaconda virtual environment named "agentomics" and will install all the necessary packages using the Poetry package manager. After installation, run ``conda activate agentomics`` to activate the environment.

## Running Experiments

To run any of the experiments, run the following command:
``python3 -m [path_to_script]``
where ``[path_to_script]`` is the path to the script you want to run, without the py file extension. For example, to run the script ``economic_simulations/three_banks.py``, you run the command
``python3 -m economic_simulations/three_banks/py``.
