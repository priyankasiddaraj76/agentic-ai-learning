from pydantic import BaseModel


class Agent(BaseModel):
    name: str
    max_retries: int
    enabled: bool


json_data = """
{
    "name": "ResearchAgent",
    "max_retries": 3,
    "enabled": true
}
"""

agent = Agent.model_validate_json(json_data)

print(agent.name)
print(agent.max_retries)