# LeadCraft Backend

A sophisticated backend system using **CrewAI**, FastAPI, and Supabase for intelligent job processing and proposal generation.

## 🚀 Features

- **AI-Powered Job Processing**: Uses CrewAI agents to refine and analyze job descriptions
- **Smart Skill Matching**: Automatically extracts and matches required skills against user profiles
- **Professional Proposal Generation**: Creates tailored proposals using AI agents
- **FastAPI Backend**: Modern, fast REST API with automatic documentation
- **Supabase Integration**: Real-time database with authentication and real-time features

## 🏗️ Architecture

### CrewAI Implementation

This project implements a sophisticated **multi-agent system** using CrewAI framework:

#### Core Components

1. **LeadCraftCrew Class** (`app/agents/crew.py`)
   - Main orchestrator for building agents, tasks, and crews
   - Configurable LLM settings (default: Gemini 2.0 Flash)
   - YAML-based configuration management

2. **Three Specialized Agents**
   - **Job Refiner Agent**: Elite requirement architect
   - **Question Generator Agent**: Clarification specialist
   - **Skill Extractor Agent**: Technical skill mapper

3. **Sequential Task Pipeline**
   - **Refine Job Description**: Creates structured requirements
   - **Generate Clarification Questions**: Professional Q&A preparation
   - **Extract Skills and Match**: Skill gap analysis

#### Process Flow

```
Raw Job Description → Refined Requirements → Clarification Questions → Skill Matching
       ↓                      ↓                      ↓                    ↓
   Input Text         Structured Document      Professional Qs      Skill Analysis
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.10+
- UV package manager
- API keys for Gemini and OpenAI

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd leadcraft-backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Fill in your API keys and configuration
   ```

4. **Run the application**
   ```bash
   uv run python main.py
   ```

## 🔧 CrewAI Usage

### Basic Usage

```python
from app.agents import LeadCraftCrew

# Initialize crew
crew = LeadCraftCrew()

# Process a job description
result = crew.run_job_description_flow(
    raw_desc="We need a FastAPI backend with authentication",
    user_skills=["Python", "FastAPI", "PostgreSQL"]
)
```

### Command Line Interface

```bash
# Run job description processing
uv run python -m app.agents.main run job_description "Job description text"

# Train the crew
uv run python -m app.agents.main train job_description 3 ./training.json

# Replay execution
uv run python -m app.agents.main replay job_description <task_id>

# Test performance
uv run python -m app.agents.main test job_description 3 gemini-1.5-pro
```

## 📁 Project Structure

```
leadcraft-backend/
├── app/
│   ├── agents/           # CrewAI implementation
│   │   ├── config/       # YAML configurations
│   │   ├── crew.py       # Main crew orchestrator
│   │   ├── main.py       # CLI interface
│   │   └── tools/        # Custom tools
│   ├── api/              # FastAPI endpoints
│   ├── core/             # Core configuration
│   ├── schemas/          # Pydantic models
│   └── services/         # External service clients
├── main.py               # Application entry point
└── pyproject.toml        # Project configuration
```

## 🎯 Agent Configurations

### Job Refiner Agent
- **Role**: Elite Project Requirement Architect
- **Goal**: Transform raw descriptions into professional requirements
- **Output**: Structured document with clear sections

### Question Generator Agent
- **Role**: Clarification Question Specialist
- **Goal**: Generate professional clarification questions
- **Output**: JSON-formatted questions by category

### Skill Extractor Agent
- **Role**: Skill & Technology Extractor
- **Goal**: Map required skills against user profiles
- **Output**: Categorized skill analysis (exact/near/missing)

## 🔄 API Endpoints

- `POST /api/v1/jobs` - Create and process job posts
- `POST /api/v1/proposals` - Generate AI-powered proposals
- `GET /api/v1/profiles` - User profile management
- `GET /api/v1/proposals` - List user proposals

## 🚀 Advanced Features

### Crew Training
```python
# Train crew with custom iterations
crew.train(n_iterations=5, filename="training_data.json")
```

### Task Replay
```python
# Replay specific task execution
crew.replay(task_id="task_123")
```

### Performance Testing
```python
# Test crew with different LLMs
crew.test(n_iterations=3, eval_llm="gemini-1.5-pro")
```

## 📊 Configuration

### LLM Settings
- **Default Model**: Gemini 2.0 Flash
- **Temperature**: 0.7 (configurable)
- **Memory**: Disabled for performance
- **Verbose**: Enabled for debugging

### Process Configuration
- **Execution**: Sequential (tasks run in order)
- **Delegation**: Disabled (agents work independently)
- **Async**: Supported but not enabled by default

## 🔍 Monitoring & Debugging

- **Verbose Mode**: Detailed execution logs
- **Task Tracking**: Individual task execution monitoring
- **Error Handling**: Comprehensive error reporting
- **Performance Metrics**: Training and testing analytics

## 🚧 Future Enhancements

- [ ] **Proposal Crew**: AI-powered proposal generation
- [ ] **Clarifications Crew**: Automated client communication
- [ ] **Multi-LLM Support**: Dynamic model selection
- [ ] **Advanced Memory**: Persistent agent memory
- [ ] **Tool Integration**: Custom tool development

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using CrewAI, FastAPI, and Supabase**
