# 🚀 CrewAI Setup Guide

Complete setup guide for your LeadCraft CrewAI system.

## 📋 Prerequisites

- **Python 3.10+** (check with `python --version`)
- **UV package manager** (install with `pip install uv`)
- **API Keys** for:
  - Google Gemini (required)
  - OpenAI (optional, for testing)
  - Supabase (required for backend)

## 🛠️ Installation Steps

### 1. Clone and Setup Project

```bash
# Navigate to your project directory
cd leadcraft-backend

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_jwt_secret
SUPABASE_PROJECT_ID=your_project_id
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Database
DATABASE_URL=your_database_url

# Optional: OpenAI API (for testing different models)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Verify Installation

```bash
# Test CrewAI installation
uv run python -c "import crewai; print(f'CrewAI Version: {crewai.__version__}')"

# Test your setup
uv run python test_crewai.py
```

## 🔧 Configuration Files

### Agents Configuration (`app/agents/config/agents.yaml`)

Your agents are configured with:
- **Job Refiner Agent**: Elite requirement architect
- **Question Generator Agent**: Clarification specialist  
- **Skill Extractor Agent**: Technical skill mapper

### Tasks Configuration (`app/agents/config/tasks.yaml`)

Tasks are configured for:
- **Refine Job Description**: Creates structured requirements
- **Generate Clarification Questions**: Professional Q&A preparation
- **Extract Skills and Match**: Skill gap analysis

### Crew Configuration (`app/agents/crew.py`)

The main orchestrator that:
- Builds agents from YAML config
- Creates tasks with dependencies
- Orchestrates crew execution

## 🧪 Testing Your Setup

### Run the Test Suite

```bash
# Run comprehensive tests
uv run python test_crewai.py
```

### Test Individual Components

```bash
# Test imports only
uv run python -c "
from app.agents.crew import LeadCraftCrew
print('✅ Import successful')
"

# Test crew creation
uv run python -c "
from app.agents.crew import LeadCraftCrew
crew = LeadCraftCrew()
crews = crew.build_crews()
print(f'✅ Built {len(crews)} crews')
"
```

### Test with Real Data

```bash
# Test job description processing
uv run python -c "
from app.agents import LeadCraftCrew
crew = LeadCraftCrew()
result = crew.run_job_description_flow(
    'We need a React app with authentication',
    ['JavaScript', 'React', 'Node.js']
)
print('✅ Processing successful')
"
```

## 🚀 Running Your System

### Command Line Interface

```bash
# Process a job description
uv run python -m app.agents.main run job_description "Job description text"

# Train the crew
uv run python -m app.agents.main train job_description 3 ./training.json

# Test performance
uv run python -m app.agents.main test job_description 2 gemini-1.5-pro
```

### Python API

```python
from app.agents import LeadCraftCrew

# Initialize crew
crew = LeadCraftCrew()

# Process job description
result = crew.run_job_description_flow(
    raw_desc="We need a FastAPI backend",
    user_skills=["Python", "FastAPI", "PostgreSQL"]
)

print(result)
```

### FastAPI Integration

Your CrewAI system is already integrated with FastAPI endpoints:

- `POST /api/v1/jobs` - Create and process jobs
- `POST /api/v1/proposals` - Generate proposals
- `GET /api/v1/profiles` - User profiles
- `GET /api/v1/proposals` - List proposals

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Check Python path
uv run python -c "import sys; print(sys.path)"

# Verify app directory structure
ls -la app/agents/
```

#### 2. YAML Syntax Errors
```bash
# Validate YAML files
uv run python -c "
import yaml
yaml.safe_load(open('app/agents/config/agents.yaml'))
print('✅ Agents YAML valid')
"
```

#### 3. API Key Issues
```bash
# Check environment variables
uv run python -c "
import os
print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')
"
```

#### 4. Memory Issues
```bash
# Check available memory
free -h  # Linux
# or
vm_stat   # macOS
```

### Debug Mode

Enable verbose logging for debugging:

```python
# In your crew configuration
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,  # Enable detailed logging
    memory=False
)
```

## 📊 Monitoring and Performance

### Enable Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use in your crew
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    memory=False
)
```

### Performance Metrics

```python
# Track execution time
import time

start_time = time.time()
result = crew.kickoff(inputs=inputs)
end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
```

## 🔄 Updating and Maintenance

### Update CrewAI

```bash
# Update to latest version
uv add crewai@latest

# Check for breaking changes
uv run python -c "
import crewai
print(f'Current version: {crewai.__version__}')
"
```

### Backup Configuration

```bash
# Backup your configs
cp -r app/agents/config/ config_backup/

# Restore if needed
cp -r config_backup/ app/agents/config/
```

## 📚 Next Steps

1. **Customize Agents**: Modify `app/agents/config/agents.yaml`
2. **Add New Tasks**: Extend `app/agents/config/tasks.yaml`
3. **Create New Crews**: Add to `app/agents/crew.py`
4. **Integrate Tools**: Extend `app/agents/tools/`
5. **Add Memory**: Enable agent memory for complex workflows
6. **Scale Up**: Add more agents and crews

## 🆘 Getting Help

- **Documentation**: Check `CREWAI_DOCUMENTATION.md`
- **Quick Start**: See `QUICKSTART.md`
- **Test Suite**: Run `test_crewai.py`
- **Official Docs**: [CrewAI Documentation](https://docs.crewai.com/)
- **Community**: [CrewAI Discord](https://discord.gg/crewai)

---

**Your CrewAI system is now ready! Run `test_crewai.py` to verify everything is working correctly.**
