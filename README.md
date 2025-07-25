# Brainstormity

An AI-powered brainstorming and idea generation application built with LangChain and LangGraph.

## Features

- AI-powered brainstorming sessions
- DAG-based conversation flows with orchestrated agent coordination
- Checkpoint and resume functionality
- RESTful API with FastAPI
- Multi-agent coordination using hybrid atomic agents with central orchestration
- Specialized agents for UVP analysis, market research, and competitor scanning
- Business model synthesis and risk assessment capabilities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Brainstormity
```

2. Create and activate a virtual environment:
```bash
python -m venv brainstormityEnv
source brainstormityEnv/bin/activate  # On Windows: brainstormityEnv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python BrainstormityBrain/main.py
```

## Architecture

### Agent Workflow
The system uses a hybrid approach combining atomic agents with central orchestration:

- **Planner/Orchestrator**: Central coordinator managing workflow and agent communication
- **Clarifier/Idea Interpreter**: Processes and clarifies user input
- **Parallel Research Agents**: UVP Critic, Market Researcher, Competitor Scanner
- **Analysis Agents**: Persona & PM-TR Analyst, Feasibility & Cost Estimator
- **Synthesis Agents**: Business Model Synthesizer, Devil's Advocate/Risk Auditor
- **Output Agents**: Action Plan Composer, Quality Gate/Evaluator

### Database Requirements
- **Vector Database**: Similarity search for market research and competitor analysis
- **MongoDB**: Structured business data, user inputs, and workflow state storage
- **Redis**: Caching, session management, and agent coordination

## Dependencies

This project uses the following key libraries:
- **LangChain Core**: Framework for building LLM applications
- **LangGraph**: Graph-based conversation flows
- **FastAPI/Starlette**: Web framework for API endpoints
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

## Project Structure

```
Brainstormity/
   BrainstormityBrain/     # Main application code
      main.py            # Entry point
   brainstormityEnv/      # Virtual environment
   requirements.txt       # Python dependencies
   README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]