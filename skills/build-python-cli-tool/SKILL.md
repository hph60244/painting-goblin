---
name: build-python-cli-tool
description: Create a Python script that solves the problem described below.
---

# Problem
<具體需求>

## Expectations
- The tool must be runnable from command line
- It should accept input args
- It should handle errors gracefully
- It comes with a markdown file as a basic agent skill for using this tool

# Workflow

1. Clarify the problem
2. Design the interface (CLI arguments)
3. Implement the script, uses $PAINTING_GOBLIN_DIR/.tmp/<name> as temporary workspace
4. Run and test it
5. Fix any issues found

# Deliverable
- A Python file under $PAINTING_GOBLIN_DIR/tools/
- The script must be executable like: `python tools/<name>.py args[1] ...`
- Create a skill in : $PAINTING_GOBLIN_DIR/skills/<name>

# Validation
After implementation, run the script and verify:
- It completes without error
- Output is correct

# If things fail
- Debug the issue
- Update the script
- Try again
