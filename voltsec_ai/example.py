"""
Example usage of voltsec_ai for code analysis.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from voltsec_ai.config import config
from voltsec_ai.tools import create_rag_tool
from voltsec_ai.agents import create_agents
from voltsec_ai.tasks import create_tasks
from crewai import Crew, Process


def run_example():
    """Run a simple example analysis."""
    
    # Use a small test directory (current directory)
    repo_path = "."
    
    print("=" * 80)
    print("VOLTSEC_AI - Example Usage")
    print("=" * 80)
    print(f"Configuration: {config}")
    print(f"Target: {repo_path}")
    print("=" * 80)
    print()
    
    try:
        # Initialize RAG tool
        print("Creating RAG tool...")
        rag_tool = create_rag_tool(repo_path)
        
        # Create agents
        print("Creating agents...")
        agents = create_agents(rag_tool)
        
        # Create tasks
        print("Creating tasks...")
        tasks = create_tasks(agents, repo_path)
        
        # Create crew
        print("Creating crew...")
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Run analysis
        print("\nStarting analysis...\n")
        result = crew.kickoff()
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("This is an example script showing how to use voltsec_ai.")
    print("For actual usage, please use: python -m voltsec_ai.main <repo_path>")
    print()
    
    # Uncomment to run the example
    # run_example()
