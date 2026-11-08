

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

STYLE = (
    "2D minimalist animation, white stickman with a round "
    "white head, black outline, thin black limbs, simple face, "
    "clean black line art, realistic present-day 2026 environment, "
    "consistent character design, no 3D"
)

def load_history():
    if HISTORY_FILE.exists():
        return set(HISTORY_FILE.read_text(
            encoding="utf-8"
        ).splitlines())
    return set()

def generate_topics(history):
    combinations = [
        f"{s} {p} {c}"
        for s in SITUATIONS
        for p in PLACES
        for c in CHALLENGES
    ]

    available = [x for x in combinations if x not in history]

    if len(available) < 2:
        raise RuntimeError("Not enough unused topics!")

    return random.sample(available, 2)

def make_scenes(topic, count, video_type):
    scenes = []

    for number in range(1, count + 1):
        if number == 1:
            action = "The stickman discovers the dangerous situation."
        elif number == 2:
            action = "The stickman looks around and studies the surroundings."
        elif number == 3:
            action = "The stickman searches for a safe place."
        elif number == count:
            action = "The stickman looks toward the horizon with hope."
        else:
            action = (
                "The stickman carefully moves through the environment "
                "and considers the next safe decision."
            )

        scenes.append(
            f"""SCENE {number}

VISUAL:
{STYLE}

LOCATION:
{topic}

ACTION:
{action}

IMAGE PROMPT:
A white minimalist stickman with a round white head,
black outline and thin black limbs. {action}
Environment: {topic}. {STYLE}.
Wide cinematic composition, clear subject, no text.

NARRATION:
The situation becomes more challenging.
The stickman must stay calm and make careful decisions.
"""
        )

    return "\n".join(scenes)

def main():
    history = load_history()
    shorts_topic, long_topic = generate_topics(history)

    SCRIPT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    shorts = f"""TITLE: {shorts_topic}

TYPE: SHORTS
LENGTH: 30-60 SECONDS

INTRO:
Imagine being completely alone.

TOPIC:
{shorts_topic}

{make_scenes(shorts_topic, 6, "SHORTS")}

ENDING:
Would you survive? Subscribe to SURVIVAL MODE.
"""

    long_video = f"""TITLE: {long_topic}

TYPE: LONG VIDEO
LENGTH: 5-7 MINUTES

INTRO:
Imagine waking up in a place where survival
depends on your decisions.

TOPIC:
{long_topic}

{make_scenes(long_topic, 30, "LONG VIDEO")}

ENDING:
Survival is about staying calm and making smart decisions.
Subscribe to SURVIVAL MODE for more scenarios.
"""

    shorts_file = SCRIPT_DIR / f"shorts_{timestamp}.txt"
    long_file = SCRIPT_DIR / f"long_{timestamp}.txt"

    shorts_file.write_text(shorts, encoding="utf-8")
    long_file.write_text(long_video, encoding="utf-8")

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(shorts_topic + "\n")
        file.write(long_topic + "\n")

    print("SHORTS CREATED:", shorts_file)
    print("LONG VIDEO CREATED:", long_file)

if __name__ == "__main__":
    main()
