"""
Agent definitions for voltsec_ai.
Defines three specialized agents for code analysis.
"""

from typing import List
from crewai import Agent
from langchain_community.llms import Ollama

from .config import config
from .tools import CodebaseRAGTool


def create_llm() -> Ollama:
    """
    Create an Ollama LLM instance with configured settings.
    
    Returns:
        Configured Ollama LLM instance
    """
    return Ollama(
        base_url=config.ollama_base_url,
        model=config.ollama_model,
        temperature=config.ollama_temperature
    )


def create_vulnerability_researcher(rag_tool: CodebaseRAGTool) -> Agent:
    """
    Create the Vulnerability Researcher agent.
    
    This agent specializes in identifying security vulnerabilities in code.
    
    Args:
        rag_tool: RAG tool for querying the codebase
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role="Security Vulnerability Researcher",
        goal="Identify and document security vulnerabilities in the codebase",
        backstory=(
            "You are an expert security researcher with years of experience "
            "in identifying vulnerabilities such as SQL injection, XSS, CSRF, "
            "insecure authentication, and other OWASP Top 10 security issues. "
            "You have a keen eye for spotting insecure code patterns and can "
            "explain security issues in detail."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
        tools=[rag_tool]
    )


def create_performance_analyst(rag_tool: CodebaseRAGTool) -> Agent:
    """
    Create the Performance Analyst agent.
    
    This agent specializes in identifying performance bottlenecks in code.
    
    Args:
        rag_tool: RAG tool for querying the codebase
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role="Performance Analyst",
        goal="Identify and document performance bottlenecks and inefficiencies in the codebase",
        backstory=(
            "You are a performance optimization expert with deep knowledge "
            "of algorithmic complexity, database query optimization, memory "
            "management, and efficient coding practices. You can spot "
            "inefficient loops, redundant operations, memory leaks, and "
            "other performance issues that could slow down applications."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
        tools=[rag_tool]
    )


def create_patch_engineer(rag_tool: CodebaseRAGTool) -> Agent:
    """
    Create the Patch Engineer agent.
    
    This agent specializes in proposing fixes for identified issues.
    
    Args:
        rag_tool: RAG tool for querying the codebase
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role="Patch Engineer",
        goal="Propose concrete code fixes and improvements for identified vulnerabilities and performance issues",
        backstory=(
            "You are a senior software engineer with expertise in secure coding "
            "practices and performance optimization. You excel at taking security "
            "vulnerabilities and performance issues and crafting practical, "
            "maintainable fixes. You provide clear code examples and explain "
            "why your proposed changes are effective."
        ),
        verbose=True,
        allow_delegation=False,
        llm=create_llm(),
        tools=[rag_tool]
    )


def create_agents(rag_tool: CodebaseRAGTool) -> dict:
    """
    Create all agents for the voltsec_ai system.
    
    Args:
        rag_tool: RAG tool for querying the codebase
        
    Returns:
        Dictionary mapping agent names to Agent instances
    """
    return {
        "vulnerability_researcher": create_vulnerability_researcher(rag_tool),
        "performance_analyst": create_performance_analyst(rag_tool),
        "patch_engineer": create_patch_engineer(rag_tool)
    }
