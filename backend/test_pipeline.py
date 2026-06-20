import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.agent_pipeline import AgentPipeline

pipeline = AgentPipeline()

result = pipeline.run_pipeline()

print("\nSYSTEM OUTPUT")
print(result)