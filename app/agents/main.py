#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import build_crews

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

"""
This main file is intended to run and manage your crews locally.
Supports: run, train, replay, test
Usage examples:
  uv run python -m leadcraft_agents.main run proposal "We need a FastAPI backend..."
  uv run python -m leadcraft_agents.main train proposal 3 ./training.json
  uv run python -m leadcraft_agents.main replay proposal <task_id>
  uv run python -m leadcraft_agents.main test proposal 3 gemini-1.5-pro
"""

from crew import LeadCraftCrew

def run_job_description_flow(raw_desc: str, user_skills: list):
    crew = LeadCraftCrew().build_crews()["job_description"]
    inputs = {
        "raw_description": raw_desc,
        "user_profile_skills": ", ".join(user_skills),
    }
    result = crew.kickoff(inputs=inputs)
    return result


def train():
    """
    Train a crew for a given number of iterations.
    Usage: main.py train <crew_name> <n_iterations> <output_filename>
    """
    if len(sys.argv) < 5:
        raise ValueError("Usage: main.py train <crew_name> <n_iterations> <output_filename>")

    crew_name, n_iterations, filename = sys.argv[2], int(sys.argv[3]), sys.argv[4]
    crews = build_crews()
    if crew_name not in crews:
        raise ValueError(f"Crew '{crew_name}' not found. Available: {list(crews.keys())}")

    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        crews[crew_name].train(n_iterations=n_iterations, filename=filename, inputs=inputs)
    except Exception as e:
        raise Exception(f"Error training crew '{crew_name}': {e}")

def replay():
    """
    Replay a crew execution from a specific task.
    Usage: main.py replay <crew_name> <task_id>
    """
    if len(sys.argv) < 4:
        raise ValueError("Usage: main.py replay <crew_name> <task_id>")

    crew_name, task_id = sys.argv[2], sys.argv[3]
    crews = build_crews()
    if crew_name not in crews:
        raise ValueError(f"Crew '{crew_name}' not found. Available: {list(crews.keys())}")

    try:
        crews[crew_name].replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"Error replaying crew '{crew_name}': {e}")

def test():
    """
    Test a crew execution.
    Usage: main.py test <crew_name> <n_iterations> <eval_llm>
    """
    if len(sys.argv) < 5:
        raise ValueError("Usage: main.py test <crew_name> <n_iterations> <eval_llm>")

    crew_name, n_iterations, eval_llm = sys.argv[2], int(sys.argv[3]), sys.argv[4]
    crews = build_crews()
    if crew_name not in crews:
        raise ValueError(f"Crew '{crew_name}' not found. Available: {list(crews.keys())}")

    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        crews[crew_name].test(n_iterations=n_iterations, eval_llm=eval_llm, inputs=inputs)
    except Exception as e:
        raise Exception(f"Error testing crew '{crew_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py [run|train|replay|test] <crew_name> ...")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run_job_description_flow()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
