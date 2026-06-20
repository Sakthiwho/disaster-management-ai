from agents.resource_agent import ResourceAgent


agent = ResourceAgent()

resources = agent.allocate_resources("CRITICAL")

print(resources)