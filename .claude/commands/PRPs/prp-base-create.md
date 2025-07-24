# Create BASE PRP

## Feature: $ARGUMENTS

## 🚨 MANDATORY: Load Project Guides First 🚨

**Before starting, load essential project documentation:**
- Read docs/PRP-FRAMEWORK.md (required for PRP creation)
- Read docs/PYTHON-GUIDE.md (for implementation standards)

---

Generate a complete PRP for feature implementation with deep and thorough research. Ensure rich context is passed to the AI through the PRP to enable one pass implementation success through self-validation and iterative refinement.

The AI agent only gets the context you are appending to the PRP and its own training data. Assume the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Research Process

> During the research process, create clear tasks and spawn as many agents and subagents as needed using the batch tools. The deeper research we do here the better the PRP will be. we optminize for chance of success and not for speed.

**⚠️ IMPORTANT: All external documentation searches MUST use Ref MCP Server:**
- Use `mcp__Ref__ref_search_documentation` for searching
- Use `mcp__Ref__ref_read_url` for reading documentation
- Do NOT use other web search tools

1. **Codebase Analysis in depth**
   - Create clear todos and spawn subagents to search the codebase for similar features/patterns Think hard and plan your approach
   - Identify all the necessary files to reference in the PRP
   - Note all existing conventions to follow
   - Check existing test patterns for validation approach
   - Use the batch tools to spawn subagents to search the codebase for similar features/patterns

2. **External Research at scale (using Ref MCP Server)**
   - Create clear todos and spawn subagents with instructions to research using Ref:
     - Use `mcp__Ref__ref_search_documentation` for finding relevant documentation
     - Use `mcp__Ref__ref_read_url` to read specific documentation pages
   - Library documentation (search with Ref and include specific URLs)
   - For critical pieces of documentation add a .md file to PRPs/ai_docs and reference it in the PRP
   - Implementation examples (search GitHub/StackOverflow/blogs via Ref)
   - Best practices and common pitfalls (search via Ref)
   - Use batch tools to spawn subagents that use Ref for all external searches

3. **User Clarification**
   - Ask for clarification if you need it

## PRP Generation

Using PRPs/templates/prp_base.md as template:

### Critical Context at minimum to Include and pass to the AI agent as part of the PRP

- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow
- **Best Practices**: Common pitfalls found during research

### Implementation Blueprint

- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- List tasks to be completed to fulfill the PRP in the order they should be completed, use the pattern in the PRP with information dense keywords

### Validation Gates (Must be Executable by the AI agent)

```bash
# Syntax/Style
ruff check --fix && mypy .

# Unit Tests
uv run pytest tests/ -v

```

The more validation gates the better, but make sure they are executable by the AI agent.
Include tests, mcp servers, and any other relevant validation gates. Get creative with the validation gates.

**_ CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP _**

**_ ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH IN DETAILED TODOS THEN START WRITING THE PRP _**

## Output

Save as: `PRPs/{feature-name}.md`

## Quality Checklist

- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context.
