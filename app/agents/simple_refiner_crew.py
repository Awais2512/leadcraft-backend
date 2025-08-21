from crewai import Agent, Task, Crew, Process, LLM
from typing import Dict, Any, List
import json
import uuid

class SimpleRefinerCrew:
    """
    Simple Job Description Refiner Crew
    
    Two main functions:
    1. Process initial raw description
    2. Refine with client answers
    """
    
    def __init__(self, model: str = "gemini/gemini-2.0-flash", temperature: float = 0.7):
        self.llm = LLM(model=model, temperature=temperature)
    
    def process_initial(self, raw_description: str) -> Dict[str, Any]:
        """
        Process initial raw description.
        
        Returns:
        - refined_description
        - title
        - project_type
        - questions (list)
        """
        
        # Create initial processing agent
        initial_agent = Agent(
            role="Project Requirements Analyst",
            goal="Analyze raw project descriptions and create refined requirements with clarification questions",
            backstory="You are an expert project analyst who specializes in understanding client requirements and identifying areas that need clarification.",
            llm=self.llm,
            verbose=True
        )
        
        # Create initial processing task
        initial_task = Task(
            description=f"""
            Analyze this raw project description and provide:
            
            1. A refined, professional description (2-3 paragraphs)
            2. A suitable project title 
            3. Project type (website, mobile-app, api, desktop-app, other)
            4. 3-5 clarification questions to ask the client
            
            Raw Description: {raw_description}
            
            Provide your response as a JSON object with this exact structure:
            {{
                "refined_description": "Professional description here...",
                "title": "Project Title",
                "project_type": "website",
                "questions": [
                    {{"id": "q1", "question": "Question 1?", "category": "Requirements", "priority": "high"}},
                    {{"id": "q2", "question": "Question 2?", "category": "Technical", "priority": "medium"}}
                ]
            }}
            """,
            expected_output="Valid JSON object with refined description, title, project type, and questions",
            agent=initial_agent
        )
        
        # Create and run crew
        crew = Crew(
            agents=[initial_agent],
            tasks=[initial_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse the JSON response
        try:
            parsed_result = json.loads(str(result))
            return parsed_result
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "refined_description": f"Refined version of: {raw_description}",
                "title": "Project Title",
                "project_type": "website",
                "questions": [
                    {"id": str(uuid.uuid4()), "question": "What is your budget range?", "category": "Budget", "priority": "high"},
                    {"id": str(uuid.uuid4()), "question": "What is your preferred timeline?", "category": "Timeline", "priority": "high"}
                ]
            }
    
    def refine_with_answers(
        self, 
        previous_refined_description: str,
        title: str,
        project_type: str,
        answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Refine description with client answers.
        
        Returns:
        - final_refined_description
        """
        
        # Create refining agent
        refining_agent = Agent(
            role="Project Requirements Finalizer",
            goal="Take refined descriptions and client answers to create final, comprehensive project requirements",
            backstory="You are an expert at incorporating client feedback into project requirements to create clear, actionable project descriptions.",
            llm=self.llm,
            verbose=True
        )
        
        # Format answers for context
        answers_context = ""
        for answer in answers:
            if not answer.get("skipped", True) and answer.get("answer"):
                answers_context += f"Q: {answer['question']}\nA: {answer['answer']}\n\n"
        
        # Create refining task
        refining_task = Task(
            description=f"""
            Take the previous refined description and integrate the client's answers to create a final, comprehensive project description.
            
            Previous Refined Description:
            {previous_refined_description}
            
            Project Title: {title}
            Project Type: {project_type}
            
            Client Answers:
            {answers_context}
            
            Create a final refined description that:
            1. Incorporates all the client's answers
            2. Is comprehensive and clear
            3. Provides enough detail for development
            4. Maintains professional tone
            
            Provide your response as a JSON object:
            {{
                "final_refined_description": "Final comprehensive description here..."
            }}
            """,
            expected_output="JSON object with final refined description",
            agent=refining_agent
        )
        
        # Create and run crew
        crew = Crew(
            agents=[refining_agent],
            tasks=[refining_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse the JSON response
        try:
            parsed_result = json.loads(str(result))
            return parsed_result
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            enhanced_description = f"{previous_refined_description}\n\nBased on client feedback:\n{answers_context}"
            return {
                "final_refined_description": enhanced_description
            }
