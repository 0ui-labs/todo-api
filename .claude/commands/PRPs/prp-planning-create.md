# Create PLANNING PRP (Advanced)

Transform rough ideas into comprehensive PRDs with rich visual documentation.

## Idea: $ARGUMENTS

## 🚨 MANDATORY: Load Project Guides First 🚨

**Before starting, load essential project documentation:**
- Read docs/PRP-FRAMEWORK.md (required for PRP creation)
- Check relevant memory files for context

---

## Discovery Process

**⚠️ All external research MUST use Ref MCP Server - do NOT use other web search tools**

1. **Concept Expansion**
   - Break down the core idea
   - Define success criteria
   - Map to business goals if provided

2. **Market & Technical Research (using Ref MCP Server)**
   - Use Ref for all external research:
     - Market analysis: `mcp__Ref__ref_search_documentation("market analysis [topic]")`
     - Competitor analysis: `mcp__Ref__ref_search_documentation("competitor analysis [topic]")`
     - Technical feasibility: `mcp__Ref__ref_search_documentation("[technology] best practices implementation")`
     - Best practice examples: `mcp__Ref__ref_search_documentation("[feature] implementation examples")`
     - Integration possibilities: `mcp__Ref__ref_search_documentation("[tech stack] integration patterns")`
   - Always use `mcp__Ref__ref_read_url` to read found documentation

3. **User Research & Clarification**
     - Ask user for the following if not provided:
     - Target user personas?
     - Key pain points?
     - Success metrics?
     - Constraints/requirements?

## PRD Generation

Using /PRPs/templates/prp_planning_base.md:

### Visual Documentation Plan
```yaml
diagrams_needed:
  user_flows:
    - Happy path journey
    - Error scenarios
    - Edge cases
  
  architecture:
    - System components
    - Data flow
    - Integration points
  
  sequences:
    - API interactions
    - Event flows
    - State changes
  
  data_models:
    - Entity relationships
    - Schema design
    - State machines
```

### Research Integration
- **Market Analysis**: Include findings in PRD
- **Technical Options**: Compare approaches
- **Risk Assessment**: With mitigation strategies
- **Success Metrics**: Specific, measurable

### User Story Development
```markdown
## Epic: [High-level feature]

### Story 1: [User need]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Specific behavior
- [ ] Edge case handling
- [ ] Performance requirement

**Technical Notes:**
- Implementation approach
- API implications
- Data requirements
```

### Implementation Strategy
- Phases with dependencies (no dates)
- Priority ordering
- MVP vs enhanced features
- Technical prerequisites

## User Interaction Points

1. **Idea Validation**
   - Confirm understanding
   - Clarify ambiguities
   - Set boundaries

2. **Research Review**
   - Share findings
   - Validate assumptions
   - Adjust direction

3. **PRD Draft Review**
   - Architecture approval
   - Risk acknowledgment
   - Success metric agreement

## Diagram Guidelines
- Use Mermaid for all diagrams
- Include legends where needed
- Show error paths
- Annotate complex flows

## Output Structure
```markdown
1. Executive Summary
2. Problem & Solution
3. User Stories (with diagrams)
4. Technical Architecture (with diagrams)
5. API Specifications
6. Data Models
7. Implementation Phases
8. Risks & Mitigations
9. Success Metrics
10. Appendices
```

Save as: `PRPs/{feature-name}-prd.md`

## Quality Checklist
- [ ] Problem clearly articulated
- [ ] Solution addresses problem
- [ ] All user flows diagrammed
- [ ] Wireframes included if needed
- [ ] Architecture visualized
- [ ] APIs fully specified with examples
- [ ] Data models included
- [ ] Dependencies identified
- [ ] Risks identified and mitigated
- [ ] Success metrics measurable
- [ ] Implementation phases logical
- [ ] Ready for implementation PRP

Remember: Great PRDs prevent implementation confusion.