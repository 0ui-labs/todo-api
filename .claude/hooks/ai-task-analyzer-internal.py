#!/usr/bin/env python3
"""
Enhanced Task Analyzer Hook for Claude Code
Performs detailed task analysis with explicit reasoning for documentation loading.
"""

import sys

def analyze_task(task):
    """Analyze task to determine required technologies and guides"""
    task_lower = task.lower()
    
    # Technology detection patterns
    tech_patterns = {
        'fastapi': ['api', 'endpoint', 'route', 'rest', 'http', 'swagger', 'openapi'],
        'sqlalchemy': ['database', 'model', 'query', 'migration', 'alembic', 'orm', 'sql'],
        'postgresql': ['postgres', 'psql', 'pg_', 'database schema'],
        'redis': ['cache', 'caching', 'rate limit', 'session', 'pub/sub'],
        'pydantic': ['validation', 'schema', 'model', 'serialize', 'deserialize'],
        'pytest': ['test', 'testing', 'coverage', 'fixture', 'mock'],
        'jwt': ['auth', 'authentication', 'token', 'login', 'security', 'password']
    }
    
    # Guide detection patterns
    guide_patterns = {
        'python_guide': ['implement', 'code', 'create', 'develop', 'refactor', 'optimize', 'fix', 'bug', 'error'],
        'prp_framework': ['plan', 'design', 'architect', 'feature', 'requirement', 'prp', 'spec']
    }
    
    detected_tech = {}
    detected_guides = {}
    
    # Detect technologies
    for tech, keywords in tech_patterns.items():
        for keyword in keywords:
            if keyword in task_lower:
                if tech not in detected_tech:
                    detected_tech[tech] = []
                detected_tech[tech].append(keyword)
    
    # Detect guides
    for guide, keywords in guide_patterns.items():
        for keyword in keywords:
            if keyword in task_lower:
                if guide not in detected_guides:
                    detected_guides[guide] = []
                detected_guides[guide].append(keyword)
    
    # Check for implicit needs
    if any(word in task_lower for word in ['create', 'implement', 'add', 'build']):
        if 'python_guide' not in detected_guides:
            detected_guides['python_guide'] = ['implicit: implementation task']
    
    if 'user' in task_lower and any(word in task_lower for word in ['registration', 'login', 'account']):
        if 'jwt' not in detected_tech:
            detected_tech['jwt'] = ['implicit: user management']
        if 'pydantic' not in detected_tech:
            detected_tech['pydantic'] = ['implicit: user validation']
    
    return detected_tech, detected_guides

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = sys.stdin.read().strip()
    
    if not task:
        return
    
    # Perform analysis
    detected_tech, detected_guides = analyze_task(task)
    
    # Print enhanced analysis
    print("🤖 ENHANCED TASK ANALYSIS WITH REASONING:")
    print("=" * 80)
    print()
    print("📋 TASK:", task)
    print()
    print("-" * 80)
    print()
    
    # Step 1: Technology Analysis
    print("🔍 STEP 1: TECHNOLOGY DETECTION & REASONING")
    print("-" * 40)
    
    tech_mapping = {
        'fastapi': '/tiangolo/fastapi',
        'sqlalchemy': '/sqlalchemy/sqlalchemy',
        'postgresql': '/postgresql/postgresql',
        'redis': '/redis/redis',
        'pydantic': '/pydantic/pydantic',
        'pytest': '/pytest-dev/pytest',
        'jwt': '/python-jose/python-jose'
    }
    
    if detected_tech:
        print("✅ DETECTED TECHNOLOGIES:")
        for tech, keywords in detected_tech.items():
            print(f"\n  📦 {tech.upper()} ({tech_mapping.get(tech, 'unknown')})")
            print(f"     Reason: Found keywords: {', '.join(set(keywords))}")
            print(f"     Action: Will load Context7 documentation")
    else:
        print("❌ No specific technologies detected from task keywords")
    
    print("\n⚠️  TECHNOLOGIES TO CONSIDER:")
    all_tech = set(tech_mapping.keys())
    not_detected = all_tech - set(detected_tech.keys())
    for tech in not_detected:
        print(f"  ❓ {tech.upper()} - Not detected, but may be needed based on task context")
    
    print()
    print("-" * 80)
    print()
    
    # Step 2: Guide Analysis
    print("📚 STEP 2: PROJECT GUIDE ANALYSIS & REASONING")
    print("-" * 40)
    
    # Python Guide Analysis
    print("\n📄 PYTHON-GUIDE.md (docs/PYTHON-GUIDE.md):")
    if 'python_guide' in detected_guides:
        print("  ✅ WILL LOAD - Reasons:")
        for keyword in detected_guides['python_guide']:
            print(f"     - Found: '{keyword}'")
        print("     - Contains: Coding standards, type hints, error handling, testing patterns")
        print("     - Needed for: Writing clean, maintainable code following project standards")
    else:
        print("  ❌ NOT LOADING - Reasons:")
        print("     - No implementation/coding keywords detected")
        print("     - Task appears to be planning/analysis only")
    
    # PRP Framework Analysis
    print("\n📄 PRP-FRAMEWORK.md (docs/PRP-FRAMEWORK.md):")
    if 'prp_framework' in detected_guides:
        print("  ✅ WILL LOAD - Reasons:")
        for keyword in detected_guides['prp_framework']:
            print(f"     - Found: '{keyword}'")
        print("     - Contains: Product requirement methodology, planning templates")
        print("     - Needed for: Structured feature planning and specification")
    else:
        print("  ❌ NOT LOADING - Reasons:")
        print("     - No planning/design keywords detected")
        print("     - Task is implementation-focused, not planning")
    
    print()
    print("-" * 80)
    print()
    
    # Step 3: Loading Instructions
    print("⚡ STEP 3: DOCUMENTATION LOADING SEQUENCE")
    print("-" * 40)
    print("\nClaude should now load documentation in this order:")
    print()
    
    priority = 1
    
    # Load guides first (they're smaller and provide context)
    if detected_guides:
        print(f"{priority}. PROJECT GUIDES:")
        if 'python_guide' in detected_guides:
            print("   - Load PYTHON-GUIDE.md using Read tool")
            priority += 1
        if 'prp_framework' in detected_guides:
            print("   - Load PRP-FRAMEWORK.md using Read tool")
            priority += 1
        print()
    
    # Then load Context7 docs
    if detected_tech:
        print(f"{priority}. CONTEXT7 DOCUMENTATION:")
        for tech in detected_tech:
            library_id = tech_mapping.get(tech)
            if library_id:
                print(f"   - Load {tech.upper()} docs: mcp__context7__get-library-docs('{library_id}')")
        print()
    
    print("-" * 80)
    print()
    print("🎯 ANALYSIS COMPLETE - Proceed with task after loading relevant documentation")
    print("=" * 80)

if __name__ == "__main__":
    main()