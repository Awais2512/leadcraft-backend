import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM


class LeadCraftCrew:
    def __init__(self, model: str = "gemini/gemini-2.0-flash", temperature: float = 0.7):
        """
        Initialize LeadCraftCrew with LLM and config directory.
        """
        self.llm = LLM(model=model, temperature=temperature)
        self.base_dir = Path(__file__).resolve().parent
        self.config_dir = self.base_dir / "config"

    def _load_yaml(self, path: Path) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def build_agents(self) -> dict:
        config = self._load_yaml(self.config_dir / "agents.yaml")
        agents = {}
        for name, cfg in config["agents"].items():
            agents[name] = Agent(
                role=cfg["role"],
                goal=cfg["goal"],
                backstory=cfg["backstory"],
                llm=self.llm,
                memory=cfg.get("memory", False),
                verbose=cfg.get("verbose", True),
                allow_delegation=cfg.get("allow_delegation", False),
            )
        return agents

    def build_tasks(self, agents: dict) -> dict:
        config = self._load_yaml(self.config_dir / "tasks.yaml")
        tasks = {}

        # First pass: create task objects
        for name, cfg in config["tasks"].items():
            tasks[name] = Task(
                description=cfg["description"],
                expected_output=cfg.get("expected_output"),
                agent=agents[cfg["agent"]],
                async_execution=cfg.get("async_execution", False),
                markdown=cfg.get("markdown", True),
            )

        # Second pass: attach contexts
        for name, cfg in config["tasks"].items():
            if "context" in cfg:
                tasks[name].context = [tasks[c] for c in cfg["context"]]

        return tasks

    def build_crews(self) -> dict:
        """
        Build and return all crews (job_description, proposal, clarifications).
        """
        agents = self.build_agents()
        tasks = self.build_tasks(agents)

        # ✅ Job Description Crew
        job_description_crew = Crew(
            agents=[
                agents["job_refiner_agent"],
                agents["question_generator_agent"],
                agents["skill_extractor_agent"],
            ],
            tasks=[
                tasks["refine_job_description"],
                tasks["generate_clarification_questions"],
                tasks["extract_skills_and_match"],
            ],
            process=Process.sequential,
            verbose=True,
            memory=False,
        )

        # TODO: Extend later with proposal crew & clarifications crew
        return {
            "job_description": job_description_crew,
        }
