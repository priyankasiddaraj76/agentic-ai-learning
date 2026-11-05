agent = {
    "name": "Research Assistant",
    "tools": ["web_search", "calculator", "file_reader"],
    "model": "GPT-6",
    "max_tool_calls": 5
}

print("Agent Name:", agent['name'])
print(agent["max_tool_calls"])
print(agent["model"])

newTool = "data_visualizer"
agent["tools"].append(newTool)

print("\nAvailable Tools:")
for tool in agent["tools"]:
    print("- ", tool)