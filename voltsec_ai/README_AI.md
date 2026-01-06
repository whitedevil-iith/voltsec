# VoltSec AI - Multi-Agent Code Analysis System

VoltSec AI is a Python-based multi-agent system that analyzes code for security vulnerabilities and performance issues using CrewAI, LangChain, and Ollama.

## Overview

VoltSec AI uses three specialized AI agents that work together to provide comprehensive code analysis:

1. **Vulnerability Researcher**: Identifies security vulnerabilities (SQL injection, XSS, CSRF, etc.)
2. **Performance Analyst**: Detects performance bottlenecks and inefficiencies
3. **Patch Engineer**: Proposes concrete fixes for identified issues

The system uses Retrieval Augmented Generation (RAG) to index and query your codebase, enabling agents to provide context-aware analysis.

## Architecture

```
┌─────────────────────────────────────────────────┐
│              VoltSec AI System                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐        ┌─────────────────┐   │
│  │  RAG Tool    │◄───────┤  Codebase Index │   │
│  │  (Chroma)    │        │  (Vector Store)  │   │
│  └──────┬───────┘        └─────────────────┘   │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐  │
│  │           CrewAI Agents                  │  │
│  ├──────────────────────────────────────────┤  │
│  │  1. Vulnerability Researcher             │  │
│  │  2. Performance Analyst                  │  │
│  │  3. Patch Engineer                       │  │
│  └──────────────────────────────────────────┘  │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐  │
│  │        Ollama LLM (Remote/Local)         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Prerequisites

### 1. Python Environment

- Python 3.9 or higher
- pip package manager

### 2. Ollama Setup

You need access to an Ollama instance (local or remote) with a suitable model.

#### Option A: Local Ollama Installation

```bash
# Install Ollama (Linux/Mac)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the default model
ollama pull nemotron-3-nano:30b

# Start Ollama server (runs on http://localhost:11434 by default)
ollama serve
```

#### Option B: Remote Ollama Node

If you have Ollama running on a remote server:

1. Ensure the Ollama server is accessible from your network
2. Note the IP address and port (default: 11434)
3. Configure the base URL using environment variables (see Configuration section)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/whitedevil-iith/voltsec.git
cd voltsec/voltsec_ai
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

VoltSec AI uses environment variables for configuration. You can set them in your shell or create a `.env` file.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Base URL of the Ollama server | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model name to use | `nemotron-3-nano:30b` |
| `OLLAMA_TEMPERATURE` | Temperature for LLM responses (0.0-1.0) | `0.7` |

### Example Configuration

#### Local Ollama

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="nemotron-3-nano:30b"
export OLLAMA_TEMPERATURE="0.7"
```

#### Remote Ollama

```bash
export OLLAMA_BASE_URL="http://192.168.1.100:11434"
export OLLAMA_MODEL="nemotron-3-nano:30b"
export OLLAMA_TEMPERATURE="0.7"
```

#### Using .env File

Create a `.env` file in the `voltsec_ai` directory:

```bash
OLLAMA_BASE_URL=http://192.168.1.100:11434
OLLAMA_MODEL=nemotron-3-nano:30b
OLLAMA_TEMPERATURE=0.7
```

Then load it before running:

```bash
# Install python-dotenv if not already installed
pip install python-dotenv

# Or use export
set -a; source .env; set +a
```

## Usage

### Basic Usage

Analyze a codebase:

```bash
python -m voltsec_ai.main /path/to/your/repository
```

### With Custom Output File

```bash
python -m voltsec_ai.main /path/to/your/repository --output my_report.md
```

### Full Example

```bash
# Set configuration
export OLLAMA_BASE_URL="http://192.168.1.100:11434"
export OLLAMA_MODEL="nemotron-3-nano:30b"

# Run analysis
python -m voltsec_ai.main ~/projects/my-app --output security_report.md
```

## Analysis Process

When you run VoltSec AI, it follows these steps:

1. **Indexing Phase**
   - Scans the target repository
   - Loads code files (supports multiple languages)
   - Creates text chunks
   - Generates embeddings using Ollama
   - Stores vectors in Chroma database

2. **Vulnerability Scanning**
   - Vulnerability Researcher agent examines code
   - Searches for security vulnerabilities
   - Uses RAG to find relevant code snippets
   - Generates detailed vulnerability report

3. **Performance Analysis**
   - Performance Analyst agent reviews code
   - Identifies bottlenecks and inefficiencies
   - Uses RAG to find problematic patterns
   - Generates performance report

4. **Patch Proposal**
   - Patch Engineer agent reviews findings
   - Proposes concrete fixes
   - Provides before/after code examples
   - Generates comprehensive patch document

5. **Report Generation**
   - Consolidates all findings
   - Saves markdown report
   - Displays summary in terminal

## Output

VoltSec AI generates a comprehensive markdown report containing:

- **Executive Summary**: Overview of findings
- **Security Vulnerabilities**: Detailed list with severity, location, and impact
- **Performance Issues**: Bottlenecks with impact assessment
- **Patch Proposals**: Concrete fixes with code examples
- **Prioritization**: Recommendations for fix order

### Example Report Structure

```markdown
# VoltSec AI - Code Analysis Report

**Repository:** /home/user/my-project
**Configuration:** Config(ollama_base_url='http://localhost:11434', ...)

---

## Security Vulnerabilities

### CRITICAL: SQL Injection in user_login.py
**Location:** src/auth/user_login.py:45
**Impact:** Attackers could access or modify database
**Description:** Raw SQL query with unsanitized user input...

## Performance Issues

### HIGH: N+1 Query Problem in api.py
**Location:** src/api/users.py:120
**Impact:** 100x slower response time for list endpoints
**Description:** Loop making individual database queries...

## Patch Proposals

### Fix for SQL Injection (Priority: CRITICAL)
**Current Code:**
```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**Proposed Fix:**
```python
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```
...
```

## Supported File Types

VoltSec AI can analyze code in multiple languages:

- Python (`.py`)
- JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`)
- C# (`.cs`)
- Go (`.go`)
- Rust (`.rs`)
- Ruby (`.rb`)
- PHP (`.php`)
- Swift (`.swift`)
- Kotlin (`.kt`)
- Scala (`.scala`)
- Shell scripts (`.sh`, `.bash`)
- Configuration files (`.yaml`, `.yml`, `.json`)
- Documentation (`.md`)

## Troubleshooting

### Issue: "Connection refused" error

**Solution:** Ensure Ollama is running and accessible:

```bash
# Test Ollama connection
curl http://localhost:11434/api/version

# Or for remote server
curl http://192.168.1.100:11434/api/version
```

### Issue: "Model not found" error

**Solution:** Pull the required model:

```bash
ollama pull nemotron-3-nano:30b
```

### Issue: Slow indexing

**Solution:** Large repositories may take time to index. The first run creates a persistent vector store in `.voltsec_ai_chroma/` which is reused on subsequent runs.

### Issue: Out of memory during indexing

**Solution:** For very large codebases, you can:
1. Exclude certain directories (modify `tools.py`)
2. Increase system RAM
3. Use a smaller chunk size in `tools.py`

## Advanced Configuration

### Customizing File Types

Edit `voltsec_ai/tools.py` and modify the `file_extensions` list in `_index_codebase()`:

```python
file_extensions = [
    ".py", ".js", ".ts",  # Add or remove extensions
    # ...
]
```

### Adjusting Chunk Size

For better or worse granularity, modify the `RecursiveCharacterTextSplitter` parameters in `tools.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Adjust chunk size
    chunk_overlap=200,    # Adjust overlap
    length_function=len,
)
```

### Changing Agent Behavior

Modify agent prompts in `agents.py` to focus on specific types of vulnerabilities or performance issues.

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: VoltSec AI Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd voltsec_ai
          pip install -r requirements.txt
      
      - name: Run VoltSec AI
        env:
          OLLAMA_BASE_URL: ${{ secrets.OLLAMA_URL }}
          OLLAMA_MODEL: nemotron-3-nano:30b
        run: |
          python -m voltsec_ai.main . --output report.md
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: report.md
```

## Performance Tips

1. **First Run**: The initial run will be slower due to codebase indexing
2. **Vector Store**: The `.voltsec_ai_chroma/` directory caches the indexed codebase
3. **Incremental Analysis**: For large codebases, consider analyzing specific directories
4. **Model Selection**: Larger models provide better analysis but require more resources

## License

This project is part of the VoltSec repository and follows its license terms.

## Support

For issues, questions, or contributions:

- GitHub Issues: https://github.com/whitedevil-iith/voltsec/issues
- Repository: https://github.com/whitedevil-iith/voltsec

## Credits

VoltSec AI is built with:

- [CrewAI](https://www.crewai.com/) - Multi-agent orchestration
- [LangChain](https://www.langchain.com/) - LLM framework
- [Ollama](https://ollama.com/) - Local LLM runtime
- [Chroma](https://www.trychroma.com/) - Vector database
