import random
from datetime import datetime

TOPICS = [
    "What If You Were Lost in a Desert?",
    "What If You Had to Survive in the Arctic?",
    "What If You Were Stranded on an Island?",
    "What If You Had No Clean Water?",
    "What If You Were Lost in a Dense Forest?",
    "What If You Had to Survive a Huge Storm?",
    "What If You Were Trapped in a Snowstorm?",
    "What If You Had to Survive Without Electricity?",
]

def create_script(topic):
    return f"""
TITLE: {topic}

[HOOK]
Imagine waking up in a place where nobody can hear you.
You have no map, no phone signal, and no idea where you are.
What would you do?

[INTRO]
Today, we explore a survival scenario:
{topic}

[SCENE 1]
First, you need to understand your surroundings.
Stay calm and avoid rushing into unknown areas.

[SCENE 2]
Your next priority is finding a safe place.
Look for shelter from weather and other hazards.

[SCENE 3]
Water is essential.
Only drink water that has been made safe to drink.

[SCENE 4]
Save your energy and make a clear plan.
If possible, contact emergency services and signal for help.

[ENDING]
Survival is not about being fearless.
It is about staying calm, thinking clearly, and making smart decisions.

Subscribe to SURVIVAL MODE for more survival scenarios.
"""

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    topic = random.choice(TOPICS)
    script = create_script(topic)

    print("================================")
    print("       SURVIVAL MODE")
    print("================================")
    print("Date:", today)
    print("Today's topic:", topic)
    print("\nGENERATED SCRIPT:\n")
    print(script)

if __name__ == "__main__":
    main()