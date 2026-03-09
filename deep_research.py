import time
from google import genai

client = genai.Client()

# 1. Start the Deep Research Agent
initial_interaction = client.interactions.create(
    input="Research the history of the Google TPUs with a focus on 2025 and 2026.",
    agent="deep-research-pro-preview-12-2025",
    background=True
)

print(f"Research started. Interaction ID: {initial_interaction.id}")

# 2. Poll for results
while True:
    interaction = client.interactions.get(initial_interaction.id)
    print(f"Status: {interaction.status}")

    if interaction.status == "completed":
        print("\nFinal Report:\n", interaction.outputs[-1].text)
        break
    elif interaction.status in ["failed", "cancelled"]:
        print(f"Failed with status: {interaction.status}")
        break

    time.sleep(10)      