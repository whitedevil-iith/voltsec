"""
Task definitions for voltsec_ai.
Defines tasks for scanning, analyzing, and patching code.
"""

from typing import List, Dict
from crewai import Task, Agent


def create_vulnerability_scan_task(agent: Agent, repo_path: str) -> Task:
    """
    Create a task for scanning code for security vulnerabilities.
    
    Args:
        agent: The vulnerability researcher agent
        repo_path: Path to the repository being analyzed
        
    Returns:
        Configured Task instance
    """
    return Task(
        description=(
            f"Analyze the codebase at '{repo_path}' for security vulnerabilities. "
            "Focus on:\n"
            "1. SQL injection vulnerabilities\n"
            "2. Cross-Site Scripting (XSS) vulnerabilities\n"
            "3. Cross-Site Request Forgery (CSRF) issues\n"
            "4. Authentication and authorization flaws\n"
            "5. Insecure cryptographic practices\n"
            "6. Input validation issues\n"
            "7. Sensitive data exposure\n"
            "8. Insecure dependencies\n"
            "9. Security misconfigurations\n"
            "10. Any other OWASP Top 10 vulnerabilities\n\n"
            "Use the codebase_query tool to search for vulnerable code patterns. "
            "Provide a detailed report with:\n"
            "- Severity level (Critical, High, Medium, Low)\n"
            "- Exact file and line location\n"
            "- Description of the vulnerability\n"
            "- Potential impact"
        ),
        expected_output=(
            "A comprehensive security report listing all identified vulnerabilities "
            "with their severity, location, description, and potential impact."
        ),
        agent=agent
    )


def create_performance_analysis_task(agent: Agent, repo_path: str) -> Task:
    """
    Create a task for analyzing code performance issues.
    
    Args:
        agent: The performance analyst agent
        repo_path: Path to the repository being analyzed
        
    Returns:
        Configured Task instance
    """
    return Task(
        description=(
            f"Analyze the codebase at '{repo_path}' for performance bottlenecks. "
            "Focus on:\n"
            "1. Inefficient algorithms (O(n²) or worse complexity)\n"
            "2. Redundant database queries (N+1 query problems)\n"
            "3. Memory leaks or excessive memory usage\n"
            "4. Inefficient loops and iterations\n"
            "5. Blocking operations in async contexts\n"
            "6. Large file I/O operations without streaming\n"
            "7. Unoptimized data structures\n"
            "8. Missing caching opportunities\n"
            "9. Resource-intensive operations in hot paths\n"
            "10. Inefficient string concatenation or regex usage\n\n"
            "Use the codebase_query tool to search for performance issues. "
            "Provide a detailed report with:\n"
            "- Impact level (High, Medium, Low)\n"
            "- Exact file and line location\n"
            "- Description of the performance issue\n"
            "- Estimated performance impact"
        ),
        expected_output=(
            "A comprehensive performance report listing all identified bottlenecks "
            "with their impact level, location, description, and estimated performance impact."
        ),
        agent=agent
    )


def create_patch_proposal_task(
    agent: Agent,
    vulnerability_task: Task,
    performance_task: Task
) -> Task:
    """
    Create a task for proposing code fixes.
    
    Args:
        agent: The patch engineer agent
        vulnerability_task: The vulnerability scan task (dependency)
        performance_task: The performance analysis task (dependency)
        
    Returns:
        Configured Task instance
    """
    return Task(
        description=(
            "Based on the security vulnerabilities and performance issues identified "
            "by the previous tasks, propose concrete code fixes and improvements. "
            "For each issue:\n"
            "1. Prioritize fixes by severity/impact\n"
            "2. Provide specific code changes (before/after)\n"
            "3. Explain why the fix resolves the issue\n"
            "4. Consider backward compatibility\n"
            "5. Suggest testing strategies\n"
            "6. Include code comments for clarity\n\n"
            "Format your response as a structured patch proposal with:\n"
            "- Issue reference (from vulnerability or performance report)\n"
            "- Priority level\n"
            "- Current code snippet\n"
            "- Proposed fix with code\n"
            "- Explanation of the fix\n"
            "- Testing recommendations"
        ),
        expected_output=(
            "A detailed patch proposal document with prioritized fixes for all "
            "identified security vulnerabilities and performance issues, including "
            "before/after code examples and explanations."
        ),
        agent=agent,
        context=[vulnerability_task, performance_task]
    )


def create_tasks(agents: Dict[str, Agent], repo_path: str) -> List[Task]:
    """
    Create all tasks for the voltsec_ai system.
    
    Args:
        agents: Dictionary of agent instances
        repo_path: Path to the repository being analyzed
        
    Returns:
        List of Task instances in execution order
    """
    vulnerability_task = create_vulnerability_scan_task(
        agents["vulnerability_researcher"],
        repo_path
    )
    
    performance_task = create_performance_analysis_task(
        agents["performance_analyst"],
        repo_path
    )
    
    patch_task = create_patch_proposal_task(
        agents["patch_engineer"],
        vulnerability_task,
        performance_task
    )
    
    return [vulnerability_task, performance_task, patch_task]
