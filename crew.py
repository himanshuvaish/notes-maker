# Updated crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class ResearchCrew:
    """Research crew for comprehensive topic analysis and crash course generation."""

    def __init__(self, agents_config, tasks_config):
        self.agents_config = agents_config
        self.tasks_config = tasks_config

    # Add a manager agent
    @agent
    def research_manager(self) -> Agent:
        """Creates the research manager agent for orchestrating multi-turn conversations."""
        return Agent(
            role="Research Manager",
            goal="Orchestrate the research process and facilitate multi-turn conversations between team members",
            backstory="You are an experienced research manager who excels at coordinating team discussions and ensuring comprehensive coverage of topics through iterative conversations.",
            verbose=True,
            allow_delegation=True,  # Key for hierarchical process
            llm="openai/gpt-4o-mini"
        )

    @agent
    def research_coordinator(self) -> Agent:
        """Creates the research coordinator agent."""
        return Agent(
            config=self.agents_config['research_coordinator'],
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        """Creates the technical researcher agent."""
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def validator(self) -> Agent:
        """Creates the validator agent."""
        return Agent(
            config=self.agents_config['validator'],
            verbose=True
        )

    # Tasks remain largely the same but with collaborative descriptions
    @task
    def coordinate_research_task(self) -> Task:
        """Task for coordinating the overall research process."""
        return Task(
            config=self.tasks_config['coordinate_research']
        )

    @task
    def conduct_research_task(self) -> Task:
        """Task for conducting technical research on the topic."""
        return Task(
            config=self.tasks_config['conduct_technical_research']
        )

    @task
    def validate_final_output_task(self) -> Task:
        """Task for validating and finalizing the research output."""
        return Task(
            config=self.tasks_config['validate_final_output'],
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates and returns the research crew with hierarchical process."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # Changed from sequential
            manager_agent=self.research_manager(),  # Add manager
            verbose=True
        )
