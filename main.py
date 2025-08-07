import os
import yaml
from dotenv import load_dotenv
from crew import ResearchCrew

# Load environment variables
load_dotenv()

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """Run the research crew."""
    try:
        inputs = {
            'topic': 'EKS'
        }

        # Load YAML configurations from config folder
        with open("config/agents.yaml", "r") as f:
            agents_config = yaml.safe_load(f)

        with open("config/tasks.yaml", "r") as f:
            tasks_config = yaml.safe_load(f)

        # Debug: Check if keys are loaded (optional - remove in production)
        print("OpenAI Key loaded:", "Yes" if os.getenv("OPENAI_API_KEY") else "No")
        print("Serper Key loaded:", "Yes" if os.getenv("SERPER_API_KEY") else "No")

        # Create and run the crew
        crew = ResearchCrew(agents_config=agents_config, tasks_config=tasks_config)
        result = crew.crew().kickoff(inputs=inputs)

        # Print the result
        print("\n\n=== FINAL REPORT ===\n\n")
        print(result.raw)

        # Save the result to file
        with open("output/report.md", "w") as f:
            f.write(result.raw)

        print("\n\nReport has been saved to output/report.md")

    except Exception as e:
        print(f"Error running crew: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()
