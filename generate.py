

import random
import math
import imageio.v2 as imageio
import numpy as np

from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

HISTORY_FILE = Path("topics_history.txt")
SCRIPT_DIR = Path("scripts")
VIDEO_DIR = Path("videos")

WIDTH = 1280
HEIGHT = 720
FPS = 12

PLACES = [
    "a deserted island", "an abandoned city",
    "a dense forest", "the Arctic",
    "a remote desert", "a snowy mountain",
    "an empty underground station", "a remote village"
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
    "Minimalist 2D stickman animation. "
    "Large round white head, thick black outline, "
    "two black eyes, curved smile, thin black limbs. "
    "Consistent character design, no 3D."
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


def make_scenes(topic, count):
    scenes = []

    for number in range(1, count + 1):
        action = (
            "The stickman discovers the dangerous situation."
            if number == 1 else
            "The stickman studies the surroundings."
            if number == 2 else
            "The stickman searches for a safe place."
            if number == 3 else
            "The stickman looks toward the horizon with hope."
            if number == count else
            "The stickman carefully explores the environment."
        )

        scenes.append(
            f"SCENE {number}\n"
            f"LOCATION: {topic}\n"
            f"ACTION: {action}\n"
            f"STYLE: {STYLE}\n"
        )

    return scenes


def draw_background(draw, topic):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(180, 215, 235))
    draw.ellipse((1000, 65, 1100, 165), fill=(255, 220, 100))

    if "island" in topic:
        draw.rectangle((0, 490, WIDTH, HEIGHT), fill=(50, 155, 190))
        draw.ellipse((180, 400, 1100, 650), fill=(225, 195, 130))

    elif "forest" in topic:
        draw.rectangle((0, 470, WIDTH, HEIGHT), fill=(95, 130, 75))
        for x in range(50, WIDTH, 180):
            draw.rectangle((x, 270, x + 25, 520), fill=(95, 65, 40))
            draw.polygon(
                [(x - 65, 330), (x + 12, 150), (x + 90, 330)],
                fill=(45, 110, 65)
            )

    elif "city" in topic or "station" in topic:
        draw.rectangle((0, 510, WIDTH, HEIGHT), fill=(95, 95, 100))
        for x in range(40, WIDTH, 190):
            draw.rectangle(
                (x, 220, x + 140, 510),
                fill=(115, 125, 135)
            )
            for y in range(260, 470, 65):
                draw.rectangle(
                    (x + 20, y, x + 50, y + 30),
                    fill=(205, 215, 220)
                )

    elif "Arctic" in topic or "snowy" in topic:
        draw.rectangle((0, 470, WIDTH, HEIGHT), fill=(235, 240, 245))
        draw.polygon(
            [(100, 480), (370, 170), (640, 480)],
            fill=(220, 230, 240)
        )
        draw.polygon(
            [(550, 480), (900, 120), (1200, 480)],
            fill=(205, 220, 235)
        )

    elif "desert" in topic:
        draw.rectangle((0, 470, WIDTH, HEIGHT), fill=(220, 185, 120))
        draw.ellipse((100, 380, 550, 590), fill=(205, 165, 105))
        draw.ellipse((700, 390, 1250, 590), fill=(215, 175, 110))

    else:
        draw.rectangle((0, 490, WIDTH, HEIGHT), fill=(125, 145, 105))
        draw.polygon(
            [(0, 490), (300, 350), (600, 490)],
            fill=(105, 135, 105)
        )
        draw.polygon(
            [(650, 490), (950, 330), (1280, 490)],
            fill=(115, 145, 110)
        )


def draw_stickman(draw, frame):
    x = 640 + int(math.sin(frame * 0.12) * 8)
    y = 330
    movement = math.sin(frame * 0.35) * 35

    # Head
    draw.ellipse(
        (x - 58, y - 58, x + 58, y + 58),
        fill="white",
        outline="black",
        width=7
    )

    # Eyes and smile
    draw.ellipse((x - 23, y - 12, x - 13, y - 2), fill="black")
    draw.ellipse((x + 13, y - 12, x + 23, y - 2), fill="black")
    draw.arc((x - 22, y + 5, x + 22, y + 38), 0, 180, fill="black", width=4)

    # Body
    draw.line((x, y + 58, x, y + 205), fill="black", width=8)

    # Arms
    draw.line(
        (x, y + 90, x - 65, y + 135 + movement),
        fill="black", width=7
    )
    draw.line(
        (x, y + 90, x + 65, y + 135 - movement),
        fill="black", width=7
    )

    # Legs
    draw.line(
        (x, y + 205, x - 48 + movement, y + 290),
        fill="black", width=8
    )
    draw.line(
        (x, y + 205, x + 48 - movement, y + 290),
        fill="black", width=8
    )


def render_video(topic, scene_count, seconds_per_scene, filename):
    VIDEO_DIR.mkdir(exist_ok=True)
    output = VIDEO_DIR / filename
    scenes = make_scenes(topic, scene_count)

    with imageio.get_writer(
        str(output),
        fps=FPS,
        codec="libx264",
        quality=7
    ) as writer:

        for scene_index, scene in enumerate(scenes):
            action = scene.split("ACTION: ")[1].split("\n")[0]

            for frame in range(seconds_per_scene * FPS):
                img = Image.new("RGB", (WIDTH, HEIGHT))
                draw = ImageDraw.Draw(img)

                draw_background(draw, topic)
                draw_stickman(draw, frame + scene_index * 10)

                draw.rectangle(
                    (0, 610, WIDTH, HEIGHT),
                    fill=(25, 25, 25)
                )

                draw.text(
                    (35, 625),
                    f"SCENE {scene_index + 1}/{scene_count}",
                    fill="white"
                )

                draw.text(
                    (35, 665),
                    action[:95],
                    fill="white"
                )

                writer.append_data(np.asarray(img))

    print("VIDEO CREATED:", output)
    return output


def main():
    history = load_history()
    shorts_topic, long_topic = generate_topics(history)

    SCRIPT_DIR.mkdir(exist_ok=True)
    VIDEO_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    shorts_scenes = make_scenes(shorts_topic, 6)
    long_scenes = make_scenes(long_topic, 30)

    shorts_file = SCRIPT_DIR / f"shorts_{timestamp}.txt"
    long_file = SCRIPT_DIR / f"long_{timestamp}.txt"

    shorts_file.write_text(
        f"TITLE: {shorts_topic}\n\n" + "\n".join(shorts_scenes),
        encoding="utf-8"
    )

    long_file.write_text(
        f"TITLE: {long_topic}\n\n" + "\n".join(long_scenes),
        encoding="utf-8"
    )

    render_video(
        shorts_topic, 6, 8,
        f"shorts_{timestamp}.mp4"
    )

    render_video(
        long_topic, 60, 12,
        f"long_{timestamp}.mp4"
    )

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(shorts_topic + "\n")
        file.write(long_topic + "\n")

    print("ALL VIDEOS CREATED!")


if __name__ == "__main__":
    main()

