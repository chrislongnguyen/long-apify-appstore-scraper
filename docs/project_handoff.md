# PROJECT HANDOFF PROTOCOL (Shutdown Procedure)

## WHEN TO RUN
Execute this protocol before logging off or switching modes.

## THE PROCEDURE

### STEP 1: COMMIT
Run in Terminal:
git add . && git commit -m "checkpoint: [describe task]"

### STEP 2: GENERATE SNAPSHOT
Run this prompt in Cursor Chat:
" @codebase Summarize the current project state for my AI PM.
Create a file named 'project_handoff_status.md' containing:
1. The Active Phase & Current Task ID.
2. A summary of 'docs/ai/requirements/README.md' (The Goal).
3. A summary of 'docs/ai/design/README.md' (The Solution & Cost).
4. A summary of 'docs/ai/planning/README.md' (The Sprint Board & Active Tasks).
5. A list of Modified Files in this session.
6. A 'Next Actions' list for when we return."

### STEP 3: THE HANDOFF
1. Copy content of `project_handoff.md`.
2. Paste into Gemini Chat to resume strategy.