# Create TASK PRP (Advanced)

Generate a comprehensive task list for focused changes with validation.

## Task: $ARGUMENTS

## 🚨 MANDATORY PRE-TASK ANALYSIS REQUIRED 🚨

**⚠️ IMPORTANT: Complete ALL steps below BEFORE starting the task!**

### 📌 REQUIRED ANALYSIS STEPS:

1. **ANALYZE** the task to identify:
   - Technologies/frameworks mentioned or implied
   - Task type (planning/documentation for TASK PRP)
   - Required documentation for research

2. **LIST AND JUSTIFY** documentation needs:
   - Technology Docs with reasons
   - Project Guides (PRP-FRAMEWORK.md) with reasons
   - Memory files needed

3. **LOAD Ref documentation**:
   - Use `mcp__Ref__ref_search_documentation` to search
   - Use `mcp__Ref__ref_read_url` to read URLs
   - Be specific in search queries

4. **LOAD project guides**:
   - Read docs/PRP-FRAMEWORK.md (required for PRP creation)
   - Read docs/PYTHON-GUIDE.md if implementation-related

5. **ONLY AFTER** completing analysis, proceed with TASK PRP creation

---

## Analysis Process

1. **Scope Definition**
   - Identify all affected files
   - Map dependencies
   - Check for side effects
   - Note test coverage

2. **Pattern Research**
   - Find similar changes in history
   - Identify conventions to follow
   - Check for helper functions
   - Review test patterns

3. **User Clarification**
   - Confirm change scope
   - Verify acceptance criteria
   - Check deployment considerations
   - Identify blockers

## PRP Generation

**READ**
Using TASK_PRP/PRPs/prp_task.md format:

### Context Section

```yaml
context:
  docs:
    - url: [API documentation]
      focus: [specific methods]

  patterns:
    - file: existing/example.py
      copy: [pattern to follow]

  gotchas:
    - issue: "Library requires X"
      fix: "Always do Y first"
```

### Task Structure

```
ACTION path/to/file:
  - OPERATION: [specific change]
  - VALIDATE: [test command]
  - IF_FAIL: [debug strategy]
  - ROLLBACK: [undo approach]
```

### Task Sequencing

1. **Setup Tasks**: Prerequisites
2. **Core Changes**: Main modifications
3. **Integration**: Connect components
4. **Validation**: Comprehensive tests
5. **Cleanup**: Remove temp code

### Validation Strategy

- Unit test after each change
- Integration test after groups
- Performance check if relevant
- Security scan for sensitive areas

## User Interaction Points

1. **Task Review**
   - Confirm task breakdown
   - Validate sequencing
   - Check completeness

2. **Risk Assessment**
   - Review potential impacts
   - Confirm rollback approach
   - Set success criteria

## Critical Elements

- Include debug patterns
- Add performance checks
- Note security concerns
- Document assumptions

## Output

Save as: `TASK_PRP/PRPs/{task-name}.md`

## Quality Checklist

- [ ] All changes identified
- [ ] Dependencies mapped
- [ ] Each task has validation
- [ ] Rollback steps included
- [ ] Debug strategies provided
- [ ] Performance impact noted
- [ ] Security checked
- [ ] No missing edge cases

Remember: Small, focused changes with immediate validation.
