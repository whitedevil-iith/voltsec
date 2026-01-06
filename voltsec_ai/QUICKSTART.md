# Quick Start Guide - VoltSec AI

This guide will help you get started with VoltSec AI in just a few minutes.

## Prerequisites

- Python 3.9+ installed
- Access to an Ollama instance (local or remote)

## Installation (Quick Method)

### Step 1: Install Ollama (if not already installed)

```bash
# On Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull nemotron-3-nano:30b

# Start Ollama (it will run in the background)
ollama serve
```

### Step 2: Install VoltSec AI

```bash
# Navigate to the voltsec_ai directory
cd voltsec_ai

# Install dependencies
pip install -r requirements.txt
```

## Configuration (Quick)

For local Ollama (default), no configuration needed. For remote Ollama:

```bash
export OLLAMA_BASE_URL="http://YOUR_IP:11434"
export OLLAMA_MODEL="nemotron-3-nano:30b"
```

## Run Your First Analysis

```bash
# Analyze a repository
python -m voltsec_ai.main /path/to/your/code

# Example: Analyze the current directory
python -m voltsec_ai.main .
```

## What Happens Next?

1. VoltSec AI will index your codebase (first run takes longer)
2. Three AI agents will analyze your code:
   - **Vulnerability Researcher**: Finds security issues
   - **Performance Analyst**: Identifies bottlenecks
   - **Patch Engineer**: Suggests fixes
3. A detailed report is saved as `voltsec_ai_report.md`

## Understanding the Output

The report includes:

- **Security Vulnerabilities**: With severity levels (Critical, High, Medium, Low)
- **Performance Issues**: With impact assessment
- **Patch Proposals**: Concrete code fixes with examples

## Common Issues

### "Connection refused"

Make sure Ollama is running:
```bash
ollama serve
```

### "Model not found"

Pull the model:
```bash
ollama pull nemotron-3-nano:30b
```

### Slow first run

This is normal - VoltSec AI is indexing your codebase. Subsequent runs will be faster.

## Next Steps

- Read the full [README_AI.md](README_AI.md) for detailed documentation
- Customize agent behavior by editing `agents.py`
- Add more file types in `tools.py`
- Integrate with CI/CD (see README_AI.md)

## Getting Help

If you encounter issues:

1. Check the [README_AI.md](README_AI.md) troubleshooting section
2. Verify your Ollama connection: `curl http://localhost:11434/api/version`
3. Check the Python version: `python --version` (needs 3.9+)

## Example Commands

```bash
# Basic analysis
python -m voltsec_ai.main ~/my-project

# With custom output file
python -m voltsec_ai.main ~/my-project --output security_audit.md

# Using remote Ollama
OLLAMA_BASE_URL=http://192.168.1.100:11434 python -m voltsec_ai.main ~/my-project

# Analyze specific directory
python -m voltsec_ai.main ~/my-project/src
```

That's it! You're ready to use VoltSec AI. 🚀
