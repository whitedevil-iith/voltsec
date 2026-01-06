"""
Main entry point for voltsec_ai.
Initializes agents and runs code analysis.
"""

import argparse
import sys
from pathlib import Path
from crewai import Crew, Process

from .config import config
from .tools import create_rag_tool
from .agents import create_agents
from .tasks import create_tasks


def main():
    """Main function to run the voltsec_ai analysis."""
    parser = argparse.ArgumentParser(
        description="voltsec_ai - Multi-agent system for code vulnerability and performance analysis"
    )
    parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository to analyze"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="voltsec_ai_report.md",
        help="Output file for the analysis report (default: voltsec_ai_report.md)"
    )
    
    args = parser.parse_args()
    
    # Validate repository path
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f"Error: Repository path '{args.repo_path}' does not exist.")
        sys.exit(1)
    
    if not repo_path.is_dir():
        print(f"Error: '{args.repo_path}' is not a directory.")
        sys.exit(1)
    
    print("=" * 80)
    print("VOLTSEC_AI - Code Security & Performance Analysis")
    print("=" * 80)
    print(f"Repository: {repo_path.absolute()}")
    print(f"Configuration: {config}")
    print("=" * 80)
    print()
    
    try:
        # Initialize RAG tool
        print("Step 1/4: Initializing RAG tool and indexing codebase...")
        rag_tool = create_rag_tool(str(repo_path.absolute()))
        print()
        
        # Create agents
        print("Step 2/4: Creating specialized agents...")
        agents = create_agents(rag_tool)
        print(f"✓ Created {len(agents)} agents")
        print()
        
        # Create tasks
        print("Step 3/4: Creating analysis tasks...")
        tasks = create_tasks(agents, str(repo_path.absolute()))
        print(f"✓ Created {len(tasks)} tasks")
        print()
        
        # Create and run crew
        print("Step 4/4: Running analysis crew...")
        print("=" * 80)
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        print()
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Save results to file
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# VoltSec AI - Code Analysis Report\n\n")
            f.write(f"**Repository:** {repo_path.absolute()}\n\n")
            f.write(f"**Configuration:** {config}\n\n")
            f.write("---\n\n")
            f.write(str(result))
        
        print(f"✓ Report saved to: {output_path.absolute()}")
        print()
        print("Results:")
        print("-" * 80)
        print(result)
        print("-" * 80)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nError during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
