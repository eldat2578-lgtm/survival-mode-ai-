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

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    topic = random.choice(TOPICS)

    print("================================")
    print("       SURVIVAL MODE")
    print("================================")
    print("Date:", today)
    print("Today's topic:", topic)
    print("Topic selected successfully!")

if __name__ == "__main__":
    main()