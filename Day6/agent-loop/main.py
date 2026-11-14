# ------------------------------------------
# MOCK DATA
# ------------------------------------------

ORDERS = {
    "ORD-1001": {
        "customer_id": "CUST-101",
        "status": "shipped",
        "total": 2499.00
    },
    "ORD-1002": {
        "customer_id": "CUST-102",
        "status": "processing",
        "total": 1599.00
    },
    "ORD-1003": {
        "customer_id": "CUST-101",
        "status": "delivered",
        "total": 4999.00
    }
}

CUSTOMERS = {
    "CUST-101": {
        "name": "Rahul",
        "membership": "premium"
    },
    "CUST-102": {
        "name": "Ananya",
        "membership": "standard"
    }
}

# ------------------------------------------
# TOOL 1: CALCULATOR
# ------------------------------------------

def calculator(
    operation: str,
    a: float,
    b: float
) -> dict:

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed")

        result = a / b

    else:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return {
        "result": result,
        "operation": operation
    }

# ------------------------------------------
# TOOL 2: ORDER LOOKUP
# ------------------------------------------

def lookup_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)

    if order is None:
        raise LookupError(f"Order {order_id} does not exist")

    return {"order_id": order_id, **order}


# ------------------------------------------
# TOOL 3: CUSTOMER LOOKUP
# ------------------------------------------

def lookup_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        raise LookupError(f"Customer {customer_id} does not exist")

    return {"customer_id": customer_id, **customer}


TOOLS = [

    {
        "type": "function",
        "name": "calculator",
        "description": (
            "Performs addition, subtraction, multiplication "
            "and division. Use it for all calculations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ]
                },
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    },

    {
        "type": "function",
        "name": "lookup_order",
        "description": (
            "Retrieves order details using an order ID. "
            "Returns customer ID, order status and total."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    },

    {
        "type": "function",
        "name": "lookup_customer",
        "description": (
            "Retrieves customer information using a customer ID. "
            "Returns customer name and membership."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"}
            },
            "required": ["customer_id"]
        }
    },

    {
        "type": "function",
        "name": "final_answer",
        "description": (
            "Call this when the task is complete or cannot "
            "be completed safely. Provide a clear answer, "
            "including any relevant failure information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "Final user-facing response"
                },
                "status": {
                    "type": "string",
                    "enum": [
                        "completed",
                        "partially_completed",
                        "failed"
                    ]
                }
            },
            "required": ["answer", "status"]
        }
    }
]

# ------------------------------------------
# TOOL DISPATCHER AND VALIDATION
# ------------------------------------------

import math

def validate_arguments(tool_name: str, args: dict) -> None:
    if not isinstance(args, dict):
        raise ValueError("Arguments must be an object")

    if tool_name == "calculator":
        if set(args) != {"operation", "a", "b"}:
            raise ValueError("Invalid calculator arguments")

        if args["operation"] not in {"add", "subtract", "multiply", "divide"}:
            raise ValueError("Invalid operation")

        for key in ("a", "b"):
            value = args[key]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{key} must be numeric")

            if not math.isfinite(value):
                raise ValueError(f"{key} must be finite")

    elif tool_name == "lookup_order":
        if set(args) != {"order_id"}:
            raise ValueError("Invalid order lookup arguments")

        if not isinstance(args["order_id"], str):
            raise ValueError("order_id must be a string")

    elif tool_name == "lookup_customer":
        if set(args) != {"customer_id"}:
            raise ValueError("Invalid customer lookup arguments")

        if not isinstance(args["customer_id"], str):
            raise ValueError("customer_id must be a string")

    else:
        raise ValueError(f"Tool is not executable: {tool_name}")


def execute_tool(tool_name: str, args: dict) -> dict:
    validate_arguments(tool_name, args)

    if tool_name == "calculator":
        return calculator(**args)

    if tool_name == "lookup_order":
        return lookup_order(**args)

    if tool_name == "lookup_customer":
        return lookup_customer(**args)

    raise ValueError(f"Unknown tool: {tool_name}")

# ------------------------------------------
# BUILDING SCRATCHPAD AND EXECUTION LOGGER
# ------------------------------------------

# scratchpad: a list of actions and their outcomes, available to the agent as context.
# agent_execution.jsonl: a permanent execution trace on your local machine.
# JSONL means JSON Lines: each line is an independent JSON object. This makes it easy to inspect or later load the logs into a data-analysis pipeline.

import json
import logging

from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR/"agent_execution.jsonl"

def log_event(event_type: str, **details):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **details
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, default=str) + "\n")

    print(
        f"[{event_type.upper()}] "
        f"{json.dumps(details, default=str)}"
    )

def add_to_scratchpad(scratchpad: list, action:str, details: dict):
    entry = {
        "step": len(scratchpad) +1,
        "action": action,
        "details": details
    }

    scratchpad.append(entry)

    log_event("scratchpad_update", entry=entry)

def get_scratchpad_summary(scratchpad: list) -> str:
    return json.dumps(scratchpad, indent=2, default=str)


# ------------------------------------------
# COMPLETE AGENT LOOP (MAIN IMPLEMENTATION)
# ------------------------------------------

# Before writing the code, understand four important decisions:
# 1. Every requested tool must be checked against our allowlist.
# 2. Tool exceptions must be converted into structured error results.
# 3. final_answer ends the loop; it is not dispatched like the other tools.
# 4. The maximum-step limit must apply even if Gemini keeps requesting more tools.

import os
import json

from dotenv import load_dotenv
from google import genai

# Configuration
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment or .env file.")

client = genai.Client(api_key=api_key)

MODEL = os.getenv("GEMINI_MODEL") or os.getenv("MODEL") or "gemini-2.0-flash"

MAX_STEPS = 8
MAX_ROUNDS = MAX_STEPS + 3

SYSTEM_INSTRUCTION = """
You are a customer support agent.

You can use these tools:
1. calculator
2. lookup_order
3. lookup_customer

Rules:

- Use tools when external data or calculations are needed.
- Never invent customer or order information.
- You may use multiple tools to complete one task.
- Review previous tool results before deciding your next action.
- If a tool fails, explain the failure and decide whether
  the task can still be completed.
- Do not repeatedly call a tool with the same failed arguments.
- Do not claim an operation succeeded unless its result confirms it.
- Keep your actions relevant to the user's request.
- When finished, call final_answer.
- If the task cannot be completed, call final_answer with
  status "failed" or "partially_completed".
- If the task is completed, call final_answer with
  status "completed".

The scratchpad supplied with tool results is execution history.
Use it to avoid repeating work.
"""

##AGENT LOOP
def run_agent(user_task: str):
    print("\n" + "=" * 65)
    print("NEW AGENT TASK")
    print("=" * 65)

    print("User:", user_task)

    scratchpad = []
    tool_steps = 0

    log_event("task_started", task=user_task, max_steps=MAX_STEPS)

    # First Gemini interaction
    interaction = client.interactions.create(
        model=MODEL,
        tools=TOOLS,
        input=user_task,
        system_instruction=SYSTEM_INSTRUCTION
    )

    # Repeat until final answer or safety limit
    for round_number in range(1, MAX_ROUNDS+1):
        log_event("model_response", round=round_number, interaction_id=interaction.id)

        function_calls = [step for step in interaction.steps
                          if step.type == "function_call"]

        # Fallback: model returned text instead of final_answer
        if not function_calls:
            answer = interaction.output_text or "I could not produce a final answer"

            log_event("agent_finished_without_final_tool", answer=answer)

            return {
                "status": "completed",
                "answer": answer,
                "scratchpad": scratchpad
            }

        function_results = []
        final_result = None

        for call in function_calls:
            tool_name = call.name
            arguments = call.arguments or {}

            log_event("tool_requested", tool=tool_name, arguments=arguments, call_id=call.id, round=round_number)
            # SPECIAL FINAL ANSWER TOOL
            if tool_name == "final_answer":
                answer = arguments.get("answer", "No final answer was supplied")
                status = arguments.get("status", "failed")
                if status not in ("completed", "partially_completed", "failed"):
                    status = "failed"

                final_result = {"status": status, "answer": answer, "scratchpad": scratchpad}
                add_to_scratchpad(scratchpad, "final_result", final_result)
                log_event("task_finished", status=status, answer=answer, tool_steps=tool_steps)
                break

            # ENFORCE MAXIMUM TOOL STEPS
            if tool_steps >= MAX_STEPS:
                result = {"status": False, "error": "Maximum tool step reached"}
                add_to_scratchpad(scratchpad, tool_name, result)
                log_event("step_limit_reached", tool=tool_name, max_steps=MAX_STEPS)
            else:
                tool_steps+=1
                # EXECUTE TOOL WITH ERROR HANDLING
                try:
                    result = execute_tool(tool_name, arguments)
                    tool_result={"success":True, "data":result}
                    log_event("tool_succeeded", tool=tool_name, result=result, tool_step=tool_steps)
                except Exception as error:
                    tool_result = {
                        "success": False,
                        "error_type": type(error).__name__,
                        "error": str(error)
                    }

                    log_event("tool_failed", tool=tool_name, error_type=type(error).__name__, error=str(error), tool_step=tool_steps)

                result = tool_result
                add_to_scratchpad(scratchpad, tool_name, result)

            result_with_context = {"tool_result": result, "scratchpad": scratchpad}

            function_results.append({
                "type": "function_result",
                "name": tool_name,
                "call_id": call.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result_with_context)
                    }
                ]
            })

        # Stop immediately when final_answer is received
        if final_result is not None:
            return final_result

        # SEND TOOL RESULTS BACK TO GEMINI
        if function_results:
            log_event("sending_results_to_model", result_count=len(function_results), tool_steps=tool_steps)
            interaction = client.interactions.create(model=MODEL, previous_interaction_id=interaction.id, input=function_results, tools=TOOLS, system_instruction=SYSTEM_INSTRUCTION)

    # MAXIMUM MODEL ROUNDS EXCEEDED
    message = "Agent stopped because it exceeded its maximum interaction rounds"
    log_event("Agent_stopped", reason=message, tool_steps=tool_steps)
    return {"status": "Failed", "answer":message, "scratchpad":scratchpad}



TEST_TASKS = [

    # 1. Basic calculation
    "Calculate 125 multiplied by 8.",

    # 2. Basic order lookup
    "Find order ORD-1001 and tell me its status.",

    # 3. Basic customer lookup
    "Find customer CUST-102 and tell me their membership.",

    # 4. Multi-tool request
    (
        "Find customer CUST-101 and order ORD-1001. "
        "Tell me the customer's name and order status."
    ),

    # 5. Calculation using order data
    (
        "Find ORD-1002 and calculate its total "
        "after adding 18% tax."
    ),

    # 6. Missing order
    "Look up order ORD-9999.",

    # 7. Missing customer
    "Find customer CUST-999.",

    # 8. Division by zero
    "Calculate 100 divided by zero.",

    # 9. Unsupported business operation
    (
        "Cancel order ORD-1001 and issue a refund. "
        "Tell me when it is complete."
    ),

    # 10. Impossible lookup and calculation
    (
        "Find order ORD-8888 and calculate its total "
        "including 18% tax."
    )
]


def run_all_tests():

    for index, task in enumerate(TEST_TASKS, start=1):

        print(f"\n\n######## TEST {index}/10 ########")

        try:
            result = run_agent(task)

            print("\nTEST RESULT:")
            print(json.dumps(result, indent=2, default=str))

        except Exception as error:

            log_event(
                "test_execution_error",
                test_number=index,
                error_type=type(error).__name__,
                error=str(error)
            )

            print(
                f"Test {index} encountered an API/application error: "
                f"{error}"
            )


if __name__ == "__main__":
    run_all_tests()
