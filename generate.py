import random
from datetime import datetime
from pathlib import Path

PLACES = [
    "a deserted island",
    "an abandoned city",
    "a dense forest",
    "the Arctic",
    "a remote desert",
    "a snowy mountain"
]

SITUATIONS = [
    "What If You Woke Up Alone in",
    "What If You Got Stranded in",
    "What If You Had to Survive in",
    "What If You Were Lost in"
]

CHALLENGES = [
    "with No Food or Water?",
    "During a Massive Storm?",
    "Without Electricity?",
    "During the Coldest Night?"
]

HISTORY_FILE = Path("topics_history.txt")
SCRIPT_DIR = Path("scripts")

def generate_topic():
    history = set()

    if HISTORY_FILE.exists():
        history = set(
            line.strip()
            for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        )

    combinations = [
        f"{situation} {place} {challenge}"
        for situation in SITUATIONS
        for place in PLACES
        for challenge in CHALLENGES
    ]

    available = [topic for topic in combinations if topic not in history]

    if not available:
        raise RuntimeError("All available topics have been used!")

    return random.choice(available)

def create_script(topic):
    return f"""TITLE: {topic}

[HOOK]
Imagine waking up in a place where nobody can hear you.
You have no phone signal and no idea what to do.
Would you survive?

[INTRO]
Today, we explore one survival scenario:
{topic}

[PART 1 - THE SITUATION]
You realize that you are completely alone.
Your first priority is to stay calm and understand your surroundings.

[PART 2 - THE FIRST CHALLENGE]
You need to find a safe place away from immediate dangers.
Avoid unnecessary risks and conserve your energy.

[PART 3 - SURVIVAL]
Think carefully about water, warmth, and communication.
If possible, contact emergency services and signal for help.

[PART 4 - THE BIGGEST MISTAKE]
Panic can make decisions harder.
Take things one step at a time and focus on safety.

[ENDING]
Survival is not about being fearless.
It is about staying calm and making smart decisions.

Subscribe to SURVIVAL MODE for more scenarios.
"""

def main():
    topic = generate_topic()

    SCRIPT_DIR.mkdir(exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")
    script = create_script(topic)

    script_file = SCRIPT_DIR / f"script_{date}.txt"
    script_file.write_text(script, encoding="utf-8")

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(topic + "\n")

    print("SURVIVAL MODE")
    print("NEW TOPIC:", topic)
    print("SCRIPT CREATED:", script_file)
    print("\n", script)

if __name__ == "__main__":
    main()