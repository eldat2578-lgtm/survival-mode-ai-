
import random
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("topics_history.txt")
SCRIPT_DIR = Path("scripts")

PLACES = [
    "a deserted island",
    "an abandoned city",
    "a dense forest",
    "the Arctic",
    "a remote desert",
    "a snowy mountain",
    "an empty underground station",
    "a remote village"
]

SITUATIONS = [
    "What If You Got Stranded in",
    "What If You Woke Up Alone in",
    "How Would You Survive in",
    "Could You Survive in"
]

CHALLENGES = [
    "with No Food or Water?",
    "During a Massive Storm?",
    "Without Electricity?",
    "During the Coldest Night?",
    "With No Way to Contact Anyone?"
]

def load_history():
    if HISTORY_FILE.exists():
        return set(
            line.strip()
            for line in HISTORY_FILE.read_text(
                encoding="utf-8"
            ).splitlines()
        )
    return set()

def generate_topic(history):
    combinations = [
        f"{situation} {place} {challenge}"
        for situation in SITUATIONS
        for place in PLACES
        for challenge in CHALLENGES
    ]

    available = [
        topic for topic in combinations
        if topic not in history
    ]

    if len(available) < 2:
        raise RuntimeError("Not enough unused topics left!")

    return random.sample(available, 2)

def create_shorts(topic):
    return f"""TITLE: {topic}

[HOOK - 0:00]
Imagine being completely alone.
No help. No signal. No easy way out.

[SCENARIO - 0:08]
{topic}

[CHALLENGE - 0:18]
Your first priority is to stay calm.
Look for a safe place and assess your surroundings.

[SURVIVAL - 0:30]
Think about water, warmth, and communication.
Avoid unnecessary risks.

[ENDING - 0:45]
Would you survive this situation?
Follow SURVIVAL MODE for more scenarios.
"""

def create_long_video(topic):
    return f"""TITLE: {topic}

[INTRODUCTION]
Imagine finding yourself in a place where
everything familiar has disappeared.
You must think carefully and make smart decisions.

[THE SITUATION]
{topic}

[CHAPTER 1 - FIRST MOMENTS]
The first challenge is understanding your situation.
Stay calm and check your surroundings.
Do not rush into unknown areas.

[CHAPTER 2 - BASIC NEEDS]
Think about safe drinking water, shelter,
and protection from the weather.
These needs should guide your decisions.

[CHAPTER 3 - MAKING A PLAN]
Divide the situation into smaller problems.
Consider the safest options available.
Avoid unnecessary risks.

[CHAPTER 4 - COMMUNICATION]
If possible, contact emergency services.
Use safe ways to signal for help.
Preserve your phone battery if you have one.

[CHAPTER 5 - COMMON MISTAKES]
Panic and rushed decisions can make things worse.
Think before acting and focus on safety.

[CONCLUSION]
Survival is not about being fearless.
It is about staying calm, thinking clearly,
and making responsible decisions.

Subscribe to SURVIVAL MODE for more scenarios.
"""

def main():
    history = load_history()
    topics = generate_topic(history)

    SCRIPT_DIR.mkdir(exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    shorts_file = SCRIPT_DIR / f"shorts_{date}.txt"
    long_file = SCRIPT_DIR / f"long_{date}.txt"

    shorts_file.write_text(
        create_shorts(topics[0]),
        encoding="utf-8"
    )

    long_file.write_text(
        create_long_video(topics[1]),
        encoding="utf-8"
    )

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        for topic in topics:
            file.write(topic + "\n")

    print("SURVIVAL MODE")
    print("SHORTS:", topics[0])
    print("LONG VIDEO:", topics[1])
    print("CREATED:", shorts_file, long_file)

if __name__ == "__main__":
    main()
