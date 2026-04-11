---
name: assign_task
description: Create and assign tasks to the painting-goblin task processing system. Use this skill when users want to add new tasks to the system, understand how the task processing workflow works, or need guidance on task file formats and placement. This skill covers task creation, file placement, system monitoring, and troubleshooting.
---

# Task Assignment Skill

This skill guides you through creating and assigning tasks to the painting-goblin task processing system. The system uses a file-based workflow with Publisher and Subscriber components to process tasks automatically.

## Quick Start

To add a task to the painting-goblin system, simply place a task file in the todo directory:

```
$PAINTING_GOBLIN_DIR\tasks\todo\
```

## Understanding the System Architecture

The painting-goblin system consists of:

1. **Publisher**: Monitors the `todo` directory and moves tasks to `doing` directory
2. **Subscriber**: Executes tasks from `doing` directory and moves them to `done` or `failed` based on results
3. **Directory Structure**:
   - `todo/`: Tasks waiting to be processed
   - `doing/`: Tasks currently being executed
   - `done/`: Successfully completed tasks
   - `failed/`: Tasks that failed during execution
   - `.log/`: Task execution logs

## How to Create a Task

### Step 1: Prepare the Task File

Task files can be in `.md` format. The system automatically adds timestamps to track processing.

**Task file content should include:**
- Clear description of what needs to be done
- Any required parameters or inputs
- Expected outputs or results
- Dependencies or prerequisites

### Step 2: Place the Task File

Copy or move your task file to the todo directory:

```bash
# Example: Create a simple task
echo "Generate weekly sales report" > "$PAINTING_GOBLIN_DIR\tasks\todo\print-42.md"
```

### Step 3: System Processing

Once a file is placed in the `todo` directory, the system automatically:

1. **Publisher detects** the new task
2. **Moves task** to `doing` directory (adds "B" timestamp prefix)
3. **Subscriber executes** the task using OpenCode
4. **Moves completed task** to `done` directory (adds "E" timestamp prefix)
5. **If execution fails**, moves task to `failed` directory

## Monitoring Task Status

### Check Task Progress

```bash
# View pending tasks
dir "$PAINTING_GOBLIN_DIR\tasks\todo\"

# View tasks in progress
dir "$PAINTING_GOBLIN_DIR\tasks\doing\"

# View completed tasks
dir "$PAINTING_GOBLIN_DIR\tasks\done\"

# View failed tasks
dir "$PAINTING_GOBLIN_DIR\tasks\failed\"
```

### Understanding Timestamps

The system adds timestamps to track task lifecycle:
- **B prefix**: Beginning timestamp (when task starts processing)
- **E prefix**: Ending timestamp (when task completes)

Example: `weekly_report.B20241215143045.md` means the task started processing at 2024-12-15 14:30:45

## Best Practices

### 1. Task Naming
- Use descriptive names: `generate_monthly_report.md` not `task1.md`
- Include context: `customer_data_analysis_Q4.md`
- Avoid special characters that might cause file system issues

### 2. Task Content
- Be specific about requirements
- Include expected outputs
- Specify any dependencies or prerequisites
- Add deadlines if time-sensitive

### 3. File Management
- Keep tasks focused on single objectives
- Split complex tasks into multiple smaller tasks
- Remove completed tasks from monitoring directories periodically

## Troubleshooting

### Common Issues and Solutions

**Issue: Task not being processed**
- Check if publisher is running: `python executor.py config.ini`
- Verify task file is in correct directory: `$PAINTING_GOBLIN_DIR\tasks\todo\`
- Check file permissions: Ensure system can read/write files

**Issue: Task stuck in doing directory**
- Check subscriber status in logs
- Verify OpenCode executable path in config.ini
- Look for errors in task execution logs

**Issue: Task moved to failed directory**
- Check `$PAINTING_GOBLIN_DIR\tasks\.log\` for execution logs
- Review task content for errors or missing information
- Verify all dependencies are available

### System Logs

Logs are stored in:
- **Executor logs**: `$PAINTING_GOBLIN_DIR\log\executor.log`
- **Task execution logs**: `$PAINTING_GOBLIN_DIR\tasks\.log\`

Check logs for detailed error information:
```bash
# View recent executor activity
tail -f "$PAINTING_GOBLIN_DIR\log\executor.log"

# View specific task execution log
type "$PAINTING_GOBLIN_DIR\tasks\.log\task_name.md.log"
```

## Getting Help

If you encounter issues:
1. Check system logs: `$PAINTING_GOBLIN_DIR\log\executor.log`
2. Verify configuration: `config.ini`
3. Ensure OpenCode is installed and accessible
4. Check file system permissions

For persistent issues, review the executor.py source code or consult system documentation.

Remember: The painting-goblin system processes tasks in order of modification time (oldest first) and supports parallel processing based on subscriber count configuration.
