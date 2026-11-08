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

def main():
    topic = generate_topic()

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(topic + "\n")

    print("SURVIVAL MODE")
    print("Date:", datetime.now().strftime("%Y-%m-%d"))
    print("NEW TOPIC:", topic)
    print("Topic saved to history!")

if __name__ == "__main__":
    main()