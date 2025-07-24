# Claude Code Hooks

This directory contains task hooks for Claude Code that automatically analyze tasks and load relevant documentation.

## Active Hooks

### ai-task-analyzer-internal.py 🤖

**Purpose**: Instructs Claude Code to analyze tasks internally and load relevant documentation

**Features:**
- No external API calls - uses your existing Claude Max plan
- Claude analyzes task context and determines needed technologies  
- Automatically identifies relevant Context7 documentation
- Determines which project guides are needed
- Faster and more reliable than external API calls

**How it works:**
1. Receives the task from the user
2. Provides Claude with structured analysis instructions
3. Lists available Context7 libraries for the project
4. Claude performs the analysis using its full context understanding
5. Claude loads relevant documentation before proceeding

**Example Output:**
```
🤖 TASK ANALYSIS REQUEST:
------------------------------------------------------------
Please analyze this task and determine:
1. What technologies/libraries are needed
2. What documentation should be loaded from Context7
3. Which project guides are relevant (PYTHON-GUIDE.md, PRP-FRAMEWORK.md)

Available Context7 libraries for this project:
- FastAPI: /tiangolo/fastapi
- SQLAlchemy: /sqlalchemy/sqlalchemy
- PostgreSQL: /postgresql/postgresql
- Redis: /redis/redis
- Pydantic: /pydantic/pydantic
- pytest: /pytest-dev/pytest
- JWT/python-jose: /python-jose/python-jose

Then proceed with the task after loading relevant documentation.
------------------------------------------------------------

TASK: implement secure user registration
```

## Disabled Hooks

The following hooks have been disabled as they are now redundant:

### ai-task-analyzer-external.py.disabled
- Used external APIs (Claude/OpenAI/Local LLM)
- Cost money for API calls
- Redundant since Claude Code already has Claude

### pre-task-analyzer.py.disabled  
- Simple keyword-based guide detection
- Limited to pattern matching
- Less intelligent than AI analysis

### technology-context-loader.py.disabled
- Keyword-based technology detection
- Static pattern matching
- Less context-aware than AI analysis

## Installation

1. Make the hook executable:
```bash
chmod +x .claude/hooks/ai-task-analyzer-internal.py
```

2. The hook runs automatically when Claude processes tasks

## Configuration

- Hooks are automatically detected by Claude Code
- To disable a hook, rename it with `.disabled` extension
- No API keys or external configuration needed

## Benefits of the New Approach

1. **Cost-effective**: Uses your existing Claude Max plan
2. **Faster**: No external API roundtrips
3. **More intelligent**: Claude has full project context
4. **Reliable**: No dependency on external services
5. **Simpler**: Less code, easier to maintain