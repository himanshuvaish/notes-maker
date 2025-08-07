import os
import yaml
from dotenv import load_dotenv
from crew import ResearchCrew

# Load environment variables
load_dotenv()

# Create output directory
os.makedirs('output', exist_ok=True)

def run():
    try:
        inputs = {
            'topic': 'EKS'
        }

        with open("config/agents.yaml", "r") as f:
            agents_config = yaml.safe_load(f)

        with open("config/tasks.yaml", "r") as f:
            tasks_config = yaml.safe_load(f)

        crew = ResearchCrew(agents_config=agents_config, tasks_config=tasks_config)
        result = crew.crew().kickoff(inputs=inputs)

        print("\n\n=== FINAL REPORT ===\n\n")
        print(result.raw)

        with open("output/report.md", "w") as f:
            f.write(result.raw)

        print("\n\nReport has been saved to output/report.md")

    except Exception as e:
        print(f"Error running crew: {e}")

if __name__ == "__main__":
    run()