from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class ResearchCrew:
    """Research crew for comprehensive topic analysis and crash course generation."""
    
    def __init__(self, agents_config=None, tasks_config=None):
        """Initialize the crew with configuration."""
        self.agents_config = agents_config or {}
        self.tasks_config = tasks_config or {}
        super().__init__()

    # ---------------------
    # Agents
    # ---------------------

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

    # ✅ Manager agent — note: no @agent decorator
    def research_manager(self) -> Agent:
        """Creates the research manager agent (not part of agents list)."""
        return Agent(
            role="Research Manager",
            goal="Oversee the entire research process and coordinate agents",
            backstory="You are an experienced leader guiding the team through complex research topics with strategic oversight.",
            verbose=True,
            allow_delegation=True,
            llm="openai/gpt-4o-mini"
        )

    # ---------------------
    # Tasks
    # ---------------------

    @task
    def coordinate_research_task(self) -> Task:
        """Task for coordinating the overall research process."""
        return Task(
            config=self.tasks_config['Coordinate Research']
        )

    @task
    def conduct_research_task(self) -> Task:
        """Task for conducting technical research on the topic."""
        return Task(
            config=self.tasks_config['Conduct Technical Research']
        )

    @task
    def validate_final_output_task(self) -> Task:
        """Task for validating and finalizing the research output."""
        return Task(
            config=self.tasks_config['Validate Final Output'],
            output_file='output/report.md'
        )

    # ---------------------
    # Crew Definition
    # ---------------------

    @crew
    def crew(self) -> Crew:
        """Creates and returns the research crew with a manager."""
        return Crew(
            agents=self.agents,  # does NOT include manager
            tasks=self.tasks,
            process=Process.hierarchical,  # manager requires hierarchical
            manager_agent=self.research_manager(),  # ✅ added manager
            verbose=True
        )
