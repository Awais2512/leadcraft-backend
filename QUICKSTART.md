# 🚀 CrewAI Quick Start Guide

Get your LeadCraft CrewAI system up and running in minutes!

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
uv sync
```

### 2. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test Your Setup
```bash
# Test the basic crew
uv run python -c "
from app.agents import LeadCraftCrew
crew = LeadCraftCrew()
print('✅ CrewAI setup successful!')
"
```

## 🎯 Quick Examples

### Process a Job Description
```python
from app.agents import LeadCraftCrew

crew = LeadCraftCrew()
result = crew.run_job_description_flow(
    raw_desc="We need a React frontend with TypeScript",
    user_skills=["JavaScript", "React", "TypeScript"]
)
print(result)
```

### Run from Command Line
```bash
# Process a job description
uv run python -m app.agents.main run job_description "We need a Python API"

# Train the crew
uv run python -m app.agents.main train job_description 2 ./training.json

# Test performance
uv run python -m app.agents.main test job_description 2 gemini-1.5-pro
```

## 🔧 Configuration

### Change LLM Model
```python
# Use OpenAI instead of Gemini
crew = LeadCraftCrew(model="gpt-4", temperature=0.3)
```

### Enable Memory
```yaml
# In app/agents/config/agents.yaml
agents:
  job_refiner_agent:
    memory: true  # Enable agent memory
```

### Add Custom Tools
```python
from app.agents.tools.custom_tool import MyCustomTool

agent = Agent(
    role="Analyst",
    tools=[MyCustomTool()],
    verbose=True
)
```

## 📊 Monitor Execution

### Enable Verbose Logging
```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,  # See detailed execution steps
    memory=False
)
```

### Track Task Results
```python
result = crew.kickoff(inputs=inputs)
print(f"Final result: {result}")
print(f"Task count: {len(result.tasks)}")
```

## 🚨 Common Issues

### 1. Import Errors
```bash
# Make sure you're in the right directory
cd leadcraft-backend
uv run python -m app.agents.main
```

### 2. API Key Issues
```bash
# Check your .env file
cat .env | grep API_KEY
```

### 3. YAML Syntax Errors
```bash
# Validate YAML files
uv run python -c "
import yaml
with open('app/agents/config/agents.yaml') as f:
    yaml.safe_load(f)
print('✅ YAML syntax valid')
"
```

## 🔄 Next Steps

1. **Customize Agents**: Modify `app/agents/config/agents.yaml`
2. **Add New Tasks**: Extend `app/agents/config/tasks.yaml`
3. **Create New Crews**: Add to `app/agents/crew.py`
4. **Integrate with API**: Use in your FastAPI endpoints
5. **Add Custom Tools**: Extend `app/agents/tools/`

## 📚 Learn More

- [Full Documentation](CREWAI_DOCUMENTATION.md)
- [Project README](README.md)
- [CrewAI Official Docs](https://docs.crewai.com/)

---

**Need help? Check the full documentation or create an issue in the repository.**
