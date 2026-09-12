# Multi-Agent Model Evaluation System

## Overview
This project implements a multi-agent system that automates key stages of a machine learning pipeline using coordinated AI agents.

The system leverages a graph-based workflow to orchestrate agents responsible for supervision, evaluation, and result generation. It integrates LLM capabilities with traditional ML evaluation and reporting to produce structured outputs such as metrics and PDF reports.

## Architecture
The system is built using a graph-based orchestration model, where each agent performs a specific responsibility and passes state to the next stage.

## Agents
Supervisor Agent
- Controls the overall workflow
- Validates inputs and execution flow
- Decides transitions between agents

Evaluation Agent
- Processes model outputs
- Computes evaluation metrics such as:
    - Accuracy
    - Precision
    - Recall
    - F1-score
- Generates structured evaluation data

Result Generation Agent
- Converts evaluation results into human-readable reports
- Uses LLM for explanation generation and metrics and tables generation
- Produces final outputs:
    - PDF reports
    - Visualizations (charts/graphs)

## Project Structure
multi_agent_model_training_demo/
├── agents           # Agent implementations (Supervisor, Evaluation, Result)
├── core             # State management and graph orchestration
├── datasets         # Input datasets
├── models           # Trained model
├── outputs          # Generated reports and artifacts
├── utils            # Logging and helper utilities
├── main.py          # Entry point
└── ui_app.py        # UI

## Installation 
- Folder setup
    cd multi_agent_model_training_demo

- Create virtual environment
    python -m venv venv
    venv\Scripts\activate # Windows

- Install dependencies
    pip install -r requirements.txt

- Configuration
    Create a .env file in the root directory
    OPENAI_API_KEY=your_api_key_here

## Usage
- Run the system
    python main.py

- Run the Streamlit UI
    streamlit run ui_app.py

