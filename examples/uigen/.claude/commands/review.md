---
description: Review current branch before merging
---
## Files Changed
!`git diff --name-only main...HEAD`

## Full Diff
!`git diff main...HEAD`

Review every changed file for:
1. Missing input validation
2. Security risks
3. Missing test coverage
4. Performance issues

Give specific, actionable feedback per file.
```