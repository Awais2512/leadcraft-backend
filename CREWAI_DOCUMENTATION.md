# CrewAI Framework Documentation

## 🎯 What is CrewAI?

**CrewAI** is a powerful framework for orchestrating role-playing autonomous AI agents. It enables you to create teams of AI agents that work together to accomplish complex tasks by assigning them specific roles and responsibilities.

### Key Concepts

- **Agents**: AI entities with specific roles, goals, and backstories
- **Tasks**: Specific assignments given to agents
- **Crews**: Teams of agents working together on related tasks
- **Process**: How tasks are executed (sequential, hierarchical, etc.)

## 🏗️ Your LeadCraft Implementation

### Architecture Overview

Your project implements a sophisticated **Job Description Processing Crew** with three specialized agents working sequentially:

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│  Raw Job Desc  │ →  │  Refined Requirements │ →  │  Clarification Qs   │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
                                ↓
                       ┌─────────────────────┐
                       │   Skill Matching    │
                       └─────────────────────┘
```

### Core Components

#### 1. LeadCraftCrew Class (`app/agents/crew.py`)

```python
class LeadCraftCrew:
    def __init__(self, model: str = "gemini/gemini-2.0-flash", temperature: float = 0.7):
        self.llm = LLM(model=model, temperature=temperature)
        self.base_dir = Path(__file__).resolve().parent
        self.config_dir = self.base_dir / "config"
```

**Features:**
- Configurable LLM (default: Gemini 2.0 Flash)
- YAML-based configuration management
- Modular agent and task building

#### 2. Agent Configuration (`app/agents/config/agents.yaml`)

Each agent has:
- **Role**: What the agent does
- **Goal**: What the agent aims to achieve
- **Backstory**: Context and expertise
- **Behavioral settings**: Memory, delegation, verbosity

#### 3. Task Configuration (`app/agents/config/tasks.yaml`)

Each task defines:
- **Description**: What needs to be done
- **Expected Output**: Format and structure
- **Agent Assignment**: Which agent handles it
- **Context**: Dependencies on other tasks

## 🔧 CrewAI Framework Features

### Supported LLMs

Your setup supports multiple LLM providers:

```python
# Gemini (default)
llm = LLM(model="gemini/gemini-2.0-flash")

# OpenAI
llm = LLM(model="gpt-4")

# Anthropic
llm = LLM(model="claude-3-sonnet")
```

### Process Types

```python
from crewai import Process

# Sequential (your current setup)
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,  # Tasks run one after another
    verbose=True
)

# Hierarchical
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.hierarchical,  # Tasks can delegate to others
    verbose=True
)

# Sequential with delegation
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
    allow_delegation=True,  # Agents can ask for help
    verbose=True
)
```

### Memory and Context

```python
# Enable memory for agents
agent = Agent(
    role="Researcher",
    goal="Research the topic",
    backstory="Expert researcher",
    memory=True,  # Agent remembers previous interactions
    verbose=True
)

# Task context (your current setup)
task = Task(
    description="Generate questions",
    agent=agent,
    context=[previous_task]  # Has access to previous task results
)
```

## 🚀 Advanced Features

### 1. Custom Tools

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class JobAnalysisTool(BaseTool):
    name: str = "Job Analysis Tool"
    description: str = "Analyzes job descriptions for requirements"
    
    def _run(self, job_text: str) -> str:
        # Your custom logic here
        return "Analysis result"

# Use in agent
agent = Agent(
    role="Analyst",
    goal="Analyze jobs",
    tools=[JobAnalysisTool()],
    verbose=True
)
```

### 2. Task Dependencies

```python
# Complex task dependencies
tasks = {
    "research": Task(description="Research topic", agent=researcher),
    "analyze": Task(description="Analyze findings", agent=analyst, context=["research"]),
    "synthesize": Task(description="Create summary", agent=writer, context=["research", "analyze"])
}
```

### 3. Crew Training

```python
# Train crew with custom data
crew.train(
    n_iterations=5,
    filename="training_data.json",
    inputs={"topic": "AI Development", "year": "2024"}
)
```

### 4. Performance Testing

```python
# Test crew performance
results = crew.test(
    n_iterations=3,
    eval_llm="gemini-1.5-pro",
    inputs={"topic": "Test Topic"}
)
```

## 📊 Best Practices

### 1. Agent Design

- **Clear Roles**: Each agent should have a distinct, focused role
- **Specific Goals**: Goals should be measurable and achievable
- **Rich Backstories**: Provide context and expertise
- **Appropriate Tools**: Give agents the tools they need

### 2. Task Design

- **Clear Descriptions**: Be specific about what needs to be done
- **Structured Outputs**: Define expected formats clearly
- **Logical Dependencies**: Plan task order carefully
- **Error Handling**: Consider what happens if tasks fail

### 3. Crew Orchestration

- **Process Selection**: Choose the right execution process
- **Memory Management**: Enable memory when needed
- **Verbose Logging**: Use for debugging and monitoring
- **Performance Optimization**: Balance speed vs. quality

## 🔍 Debugging and Monitoring

### Verbose Mode

```python
# Enable detailed logging
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,  # Shows detailed execution steps
    memory=False
)
```

### Task Tracking

```python
# Monitor individual task execution
result = crew.kickoff(inputs=inputs)
print(f"Task results: {result}")
```

### Error Handling

```python
try:
    result = crew.kickoff(inputs=inputs)
except Exception as e:
    print(f"Crew execution failed: {e}")
    # Handle error appropriately
```

## 🚧 Extending Your Implementation

### 1. Add New Agents

```yaml
# app/agents/config/agents.yaml
agents:
  proposal_writer_agent:
    role: "Professional Proposal Writer"
    goal: "Create compelling project proposals"
    backstory: "Expert in writing winning proposals..."
    allow_delegation: false
    verbose: true
```

### 2. Add New Tasks

```yaml
# app/agents/config/tasks.yaml
tasks:
  write_proposal:
    description: "Write a professional proposal based on requirements"
    expected_output: "Complete proposal document"
    agent: proposal_writer_agent
    context:
      - refine_job_description
      - extract_skills_and_match
```

### 3. Create New Crews

```python
# In crew.py
proposal_crew = Crew(
    agents=[
        agents["proposal_writer_agent"],
        agents["reviewer_agent"]
    ],
    tasks=[
        tasks["write_proposal"],
        tasks["review_proposal"]
    ],
    process=Process.sequential,
    verbose=True
)

return {
    "job_description": job_description_crew,
    "proposal": proposal_crew,  # New crew
}
```

## 📚 Resources and References

### Official Documentation
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [CrewAI Examples](https://github.com/joaomdmoura/crewAI/tree/main/examples)

### Community Resources
- [CrewAI Discord](https://discord.gg/crewai)
- [CrewAI Blog](https://blog.crewai.com/)

### Related Technologies
- [LangChain](https://python.langchain.com/) - LLM application framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

## 🔄 Version Compatibility

### CrewAI 0.165.1 Features

Your current version (0.165.1) includes:
- ✅ Multi-LLM support
- ✅ Custom tools integration
- ✅ Task dependencies and context
- ✅ Crew training and testing
- ✅ Memory management
- ✅ Process orchestration
- ✅ Verbose logging and debugging

### Migration Notes

When upgrading CrewAI:
1. Check breaking changes in release notes
2. Test agent configurations
3. Verify task dependencies
4. Update import statements if needed

---

**This documentation covers CrewAI framework fundamentals and your specific implementation. For the latest updates, always refer to the official CrewAI documentation.**
