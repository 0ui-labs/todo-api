# Review and Save Command

Please use the Task tool to execute the /zen:review command, then automatically save the comprehensive code review results to the PRPs/code-reviews/issues folder.

## Instructions:
1. Execute `/zen:review` using the Task tool with this exact prompt
2. After the review completes, create a new markdown file in PRPs/code-reviews/issues/
3. Determine the next ID by checking existing files in that directory
4. Use naming format: `{ID}-code-review-{DATE}-comprehensive-todo-api.md`
5. Format the review with all sections from the zen:review output

## Required Sections:
- Executive Summary
- Overall Scores by Category
- Issues by Severity (Critical, High, Medium, Low)
- Positive Findings
- Recommendations (Immediate, Short Term, Long Term)
- Production Readiness Checklist
- Conclusion

The review should maintain the same comprehensive format as the MCP tool output.