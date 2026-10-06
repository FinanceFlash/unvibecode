# Product and Business Guide

## People and systems
- **User**: Submits the task.
- **Agent Orchestrator**: The system managing the agent lifecycle.
- **LLM Provider**: The intelligence model.
- **Tool Registry**: The directory of available tools and permissions.
- **External Tool/Service**: The system executing the side effect.

## Things created or changed
- **Task Request**: The initial instruction.
- **Execution Plan**: The agent's intended sequence of actions.
- **Tool Call**: A specific request to execute a tool.
- **Tool Result**: The output or error from a tool.
- **Final Outcome**: The result of the task.

## Stages
- **Task Received**: Task is accepted.
- **Planning**: Agent formulates a plan.
- **Tool Selection**: Agent decides which tool to call.
- **Authorization**: System verifies permission for the tool.
- **Execution**: Tool is invoked.
- **Result Validation**: Tool output is processed.
- **Completion/Escalation**: Task is resolved or escalated.
