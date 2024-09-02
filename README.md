# AI/ML Template

## Introduction

This is a template repository for AI/ML application development and research. The goal of this template is to provide commonly used packages with reproducible environments with proper dependency environment and multi-platform support.

## Tackling Environment Complexity

I am using Conda and Poetry together to tackle the task of managing a complex AI/ML environment. Conda is used to create isolated environments while Poetry is used to manage packages and ensure dependency resolution ([article](https://medium.com/@silvinohenriqueteixeiramalta/conda-and-poetry-a-harmonious-fusion-8116895b6380#:~:text=Conda%20and%20Poetry%20are%20well,package%20management%20and%20dependency%20resolution.)).

## Tackling Command Line Complexity

I am using a Makefile to automate shell commands to create and build the conda environment and run test files. I am creating this Makefile from scratch using this [article](https://medium.com/@silvinohenriqueteixeiramalta/conda-and-poetry-a-harmonious-fusion-8116895b6380#:~:text=Conda%20and%20Poetry%20are%20well,package%20management%20and%20dependency%20resolution.).

## Tackling Reproducible Environments

I am using conda-lock to generate a concrete lock file of all the dependencies required by conda (and for Python and Poetry). This allows for reproducibility as the exact versions and download links used to create the environment are saved ([link to conda-lock GitHub](https://github.com/conda/conda-lock)).

> ℹ️ Every time environment.yaml is changed, run the following command to ensure conda-lock.yml is refereshed:
```bash
make lock-conda
```
