
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

# Arguments for the search tool
class searchArgumments(StrictModel):
    query: str = Field(min_length=3)

# Arguments for the calculator tool
class calculatorArgumments(StrictModel):
    expression: str = Field(min_length=1)

# Arguments for the final response
class FinishArguments(StrictModel):
    answer: str = Field(min_length=1)

# Search tool action
class SearchAction(StrictModel):
    name: Literal["search"]
    arguments: searchArgumments

# Calculator tool action
class CalculatorAction(StrictModel):
    name: Literal["calculator"]
    arguments: calculatorArgumments

# Final response action
class FinishAction(StrictModel):
    name: Literal["finish"]
    arguments: FinishArguments

# The action must match one of the three actions, and the discriminator is the "name" field
AgentAction = Annotated[SearchAction | CalculatorAction | FinishAction, 
                        Field(discriminator="name")]

class AgentResponse(StrictModel):
    plan_summary: str
    action: AgentAction

def main() -> None:
    json_data = """
    {
        "plan_summary": "I need to search for recent AI developments.",
        "action": {
            "name": "search",
            "arguments": {
                "query": "Latest developments in Agentic AI"
            }
        }
    }
    """

    try:
        agent_response = AgentResponse.model_validate_json(json_data)
        print("Agent response is valid:")
        print("Plan Summary:", agent_response.plan_summary)
        print("Action Name:", agent_response.action.name)
        print("Action Arguments:", agent_response.action.arguments)
    except ValidationError as e:
        print("Error occurred while validating agent response:")
        print(e)

    json_data2 = """
        {
            "plan_summary": "I need to add 2 and 3.",
            "action": {
                "name": "calculator",
                "arguments": {
                    "expression": "The sum is 5"
                }
            }
        }
        """

    try:
        agent_response = AgentResponse.model_validate_json(json_data2)
        print("Agent response is valid:")
        print("Plan Summary:", agent_response.plan_summary)
        print("Action Name:", agent_response.action.name)
        print("Action Arguments:", agent_response.action.arguments)
    except ValidationError as e:
        print("Error occurred while validating agent response:")
        print(e)


if __name__ == "__main__":
    main()