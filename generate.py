import random
from datetime import datetime

situations = [
    "waking up alone",
    "getting stranded",
    "being trapped",
    "losing all communication",
    "having no supplies",
    "getting lost"
]

places = [
    "in a mysterious forest",
    "on a deserted island",
    "in the Arctic",
    "in a remote desert",
    "inside an abandoned city",
    "in the mountains"
]

challenges = [
    "with no food or water",
    "during a powerful storm",
    "with no electricity",
    "during the coldest night",
    "with limited resources"
]

def generate_topic():
    return (
        "What If You Were "
        + random.choice(situations)
        + " "
        + random.choice(places)
        + " "
        + random.choice(challenges)
        + "?"
    )

def main():
    topic = generate_topic()

    print("SURVIVAL MODE")
    print("Date:", datetime.now().strftime("%Y-%m-%d"))
    print("NEW TOPIC:", topic)

if __name__ == "__main__":
    main()