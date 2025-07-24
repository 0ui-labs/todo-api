#!/usr/bin/env python3
"""
Task Analysis Hook for Claude Code
Instructs Claude to perform AI-powered analysis before executing any task.
"""

import sys


def main():
    """Main entry point"""
    import json

    # Read JSON input from stdin
    try:
        input_data = sys.stdin.read()
        if input_data:
            data = json.loads(input_data)
            # Extract the user prompt from the JSON
            task = data.get('user_prompt', '')
        else:
            task = ""
    except:
        # Fallback for command line testing
        if len(sys.argv) > 1:
            task = " ".join(sys.argv[1:])
        else:
            task = ""

    if not task:
        return

    # Print mandatory instructions for Claude
    print("🚨 MANDATORY PRE-TASK ANALYSIS REQUIRED 🚨")
    print("=" * 80)
    print()
    print("⚠️  IMPORTANT: You MUST complete ALL steps below BEFORE starting the task!")
    print()
    print(f"📋 USER TASK: {task}")
    print()
    print("📌 REQUIRED ANALYSIS STEPS:")
    print("-" * 40)
    print()
    print("1️⃣  ANALYZE the task using your AI capabilities to identify:")
    print("   • What technologies/frameworks are mentioned or implied")
    print("   • What type of task this is (implementation, planning, debugging, etc.)")
    print("   • What documentation will be needed")
    print()
    print("2️⃣  LIST AND JUSTIFY your documentation needs:")
    print("   Create a detailed list with reasoning:")
    print()
    print("   📋 REQUIRED DOCUMENTATION:")
    print("   ├─ Technology Docs:")
    print("   │  • [Tech Name] - REASON: Why this is needed for the task")
    print("   │  • [Tech Name] - REASON: Specific aspect needed (e.g., 'authentication flow')")
    print("   │")
    print("   ├─ Project Guides:")
    print("   │  • PYTHON-GUIDE.md - REASON: [Why needed] OR 'NOT NEEDED: [Why not]'")
    print("   │  • PRP-FRAMEWORK.md - REASON: [Why needed] OR 'NOT NEEDED: [Why not]'")
    print("   │")
    print("   └─ Additional Context:")
    print("      • Memory files - REASON: [Which ones and why]")
    print()
    print("   ⚠️  You MUST provide clear reasoning for EACH documentation choice!")
    print()
    print("3️⃣  THINK about implicit requirements:")
    print("   • 'user registration' → needs authentication (JWT, Pydantic)")
    print("   • 'API endpoint' → needs FastAPI documentation")
    print("   • 'database' → needs SQLAlchemy, PostgreSQL docs")
    print("   • 'caching' → needs Redis documentation")
    print()
    print("4️⃣  LOAD Context7 documentation for EACH identified technology:")
    print("   a) First use mcp__context7__resolve-library-id to find the correct library")
    print("   b) Then use mcp__context7__get-library-docs with specific topic/tokens parameters")
    print()
    print("   Examples:")
    print("   • FastAPI: resolve-library-id('fastapi') → get-library-docs with topic='endpoints'")
    print("   • SQLAlchemy: resolve-library-id('sqlalchemy') → get-library-docs with topic='orm'")
    print("   • Pydantic: resolve-library-id('pydantic') → get-library-docs with topic='validation'")
    print("   • JWT: resolve-library-id('python-jose') → get-library-docs with topic='authentication'")
    print()
    print("   ⚠️  IMPORTANT: Always specify 'topic' parameter to load only relevant sections!")
    print("   ⚠️  Use 'tokens' parameter (default 10000) to control documentation size")
    print()
    print("5️⃣  LOAD project guides based on task type:")
    print("   • Implementation/coding → Read docs/PYTHON-GUIDE.md")
    print("   • Planning/design → Read docs/PRP-FRAMEWORK.md")
    print()
    print("6️⃣  ONLY AFTER completing steps 1-5, proceed with the actual task")
    print()
    print("-" * 80)
    print()
    print("💡 EXAMPLE ANALYSIS:")
    print("Task: 'Implement user registration with email validation'")
    print("→ Technologies: FastAPI (API), JWT (auth), Pydantic (validation), SQLAlchemy (DB)")
    print("→ Guides: PYTHON-GUIDE.md (implementation)")
    print("→ Action: Load all 4 Context7 docs + Python guide BEFORE coding")
    print()
    print("=" * 80)
    print("⏸️  PAUSE NOW and complete the analysis steps above!")
    print("=" * 80)

if __name__ == "__main__":
    main()
