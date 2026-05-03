---
name: build-python-cli-app
description: Create a Python script that solves the problem below. It should follow constraints and complete all tasks.
---

# Problem

<待解問題>

# Constraints

## <具體約束>
- <約束理由>
- ...

# Tasks

## <子任務>

### Contract
- <規格>
- ...

### Acceptance
- <測項>
- ...

# Workflow

1. Clarify the problem
2. Clarify all constraints
3. Use $AGENT_CWD/.tmp/<name> as temporary workspace
4. Create a empty $AGENT_CWD/apps/<name>/<name>.py script
5. For each task
    1. Clarify all specs
    2. Implement task in <name>.py script
    3. Run the script and verify:
        - It completes without error
        - Output is correct
    4. If things fail:
        - Debug the issue
        - Update the script
        - Try again
    5. If things fail too many times:
        - Rollback and restart from previous task
6. Create a $AGENT_CWD/apps/<name>/requirements.txt file if needed
7. Create a skill under $AGENT_CWD/apps/<name> by $AGENT_CWD/skills/make-skill-template
