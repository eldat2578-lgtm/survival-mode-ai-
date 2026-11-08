"""SURVIVAL MODE video generator — animated story v1.

Creates consistent 2D stickman scenes with scene-specific actions, camera motion,
environment details and readable story captions. Rendering stays dependency-light
so it can run in GitHub Actions.
"""
import math
import random
from datetime import datetime
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HISTORY_FILE = Path("topics_history.txt")
SCRIPT_DIR = Path("scripts")
VIDEO_DIR = Path("videos")
WIDTH, HEIGHT, FPS = 1280, 720, 12
GROUND_Y = 535

PLACES = [
    "a deserted island", "an abandoned city", "a dense forest", "the Arctic",
    "a remote desert", "a snowy mountain", "an empty underground station",
    "a remote village"
]
SITUATIONS = [
    "What If You Got Stranded in", "What If You Woke Up Alone in",
    "How Would You Survive in", "Could You Survive in"
]
CHALLENGES = [
    "with No Food or Water?", "During a Massive Storm?",
    "Without Electricity?", "During the Coldest Night?",
    "With No Way to Contact Anyone?"
]
STYLE = ("Minimalist 2D animation; one consistent white round-headed stickman, "
         "bold black outline, simple expressive face, thin articulated limbs; "
         "clean cinematic composition; absolutely no 3D.")

# Each beat changes the character's intention and pose, rather than repeating
# the same generic movement in every scene.
BEATS = [
    ("arrival", "The character realizes they are alone and takes in the surroundings.", "look"),
    ("observe", "They carefully observe the area and notice useful landmarks.", "shade"),
    ("move", "They walk to a more sheltered, open and visible location.", "walk"),
    ("inspect", "They inspect the surroundings and think through their options.", "crouch"),
    ("prepare", "They organize what they have and make a simple plan.", "work"),
    ("weather", "The weather changes; they pause and choose a safer position.", "brace"),
    ("signal", "They move to a visible place and try to attract attention.", "signal"),
    ("wait", "They rest, stay alert and conserve their energy.", "sit"),
    ("hope", "A distant sign gives them hope; they look toward the horizon.", "point"),
    ("finish", "They face the horizon, ready for the next safe step.", "look"),
]

def load_history():
    return set(HISTORY_FILE.read_text(encoding="utf-8").splitlines()) if HISTORY_FILE.exists() else set()

def generate_topics(history):
    choices = [f"{s} {p} {c}" for s in SITUATIONS for p in PLACES for c in CHALLENGES]
    available = [item for item in choices if item not in history]
    if len(available) < 2:
        raise RuntimeError("Not enough unused topics; review topics_history.txt.")
    return random.sample(available, 2)

def make_scenes(topic, count):
    scenes = []
    for i in range(count):
        beat = BEATS[min(len(BEATS) - 1, int(i * len(BEATS) / count))]
        scenes.append({
            "number": i + 1,
            "beat": beat[0],
            "action": beat[1],
            "pose": beat[2],
            "location": topic,
        })
    return scenes

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

FONT = load_font(25)
SMALL = load_font(18)
TITLE = load_font(34, True)

def palette(topic):
    if "Arctic" in topic or "snowy" in topic:
        return ((160, 190, 210), (225, 235, 242), (100, 130, 150))
    if "desert" in topic:
        return ((235, 190, 130), (220, 180, 120), (150, 115, 80))
    if "island" in topic:
        return ((125, 195, 215), (225, 200, 145), (65, 145, 155))
    if "forest" in topic:
        return ((155, 190, 160), (95, 125, 85), (50, 90, 65))
    if "city" in topic or "station" in topic:
        return ((165, 180, 195), (105, 115, 125), (65, 75, 85))
    return ((175, 200, 180), (125, 145, 105), (75, 100, 75))

def draw_background(draw, topic, t, camera):
    sky, ground, accent = palette(topic)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=sky)
    # Slow drifting clouds and distant silhouettes create gentle parallax.
    for i in range(4):
        x = int((i * 360 + t * (5 + i * 2) - camera * 0.25) % (WIDTH + 220)) - 110
        y = 95 + (i % 2) * 70
        draw.ellipse((x, y, x + 100, y + 30), fill=(235, 240, 238))
        draw.ellipse((x + 25, y - 14, x + 78, y + 25), fill=(235, 240, 238))
    draw.rectangle((0, GROUND_Y, WIDTH, HEIGHT), fill=ground)

    if "forest" in topic:
        for i in range(-1, 9):
            x = int(i * 175 - camera * 0.45) % (WIDTH + 200) - 100
            draw.rectangle((x + 55, 270, x + 78, GROUND_Y), fill=(95, 70, 48))
            draw.polygon([(x - 5, 340), (x + 66, 150), (x + 140, 340)], fill=accent)
            draw.polygon([(x + 10, 405), (x + 66, 230), (x + 125, 405)], fill=accent)
    elif "city" in topic or "station" in topic:
        for i in range(-1, 8):
            x = int(i * 190 - camera * 0.35) % (WIDTH + 220) - 110
            draw.rectangle((x, 220, x + 145, GROUND_Y), fill=(105, 115, 128))
            for wy in range(250, 465, 65):
                draw.rectangle((x + 20, wy, x + 52, wy + 32), fill=(215, 220, 215))
                draw.rectangle((x + 85, wy, x + 117, wy + 32), fill=(215, 220, 215))
    elif "Arctic" in topic or "snowy" in topic:
        for i in range(3):
            x = i * 480 - int(camera * 0.2)
            draw.polygon([(x - 80, GROUND_Y), (x + 160, 150 + i * 45), (x + 400, GROUND_Y)], fill=(220, 230, 238))
            draw.polygon([(x + 160, 150 + i * 45), (x + 100, 255 + i * 45), (x + 220, 255 + i * 45)], fill=(250, 250, 248))
    elif "desert" in topic:
        for i in range(4):
            x = i * 390 - int(camera * 0.25)
            draw.ellipse((x - 100, 390, x + 360, 625), fill=(205, 160, 105))
    elif "island" in topic:
        draw.rectangle((0, GROUND_Y + 75, WIDTH, HEIGHT), fill=(65, 155, 185))
        draw.ellipse((-120 - int(camera * .15), 400, 500, 610), fill=(225, 195, 140))
        draw.ellipse((650 - int(camera * .15), 420, 1300, 625), fill=(225, 195, 140))
    else:
        for i in range(5):
            x = i * 330 - int(camera * .25)
            draw.ellipse((x - 100, 400, x + 260, 620), fill=accent)

def line(draw, points, width=7):
    draw.line(points, fill=(20, 22, 25), width=width, joint="curve")

def draw_character(draw, x, ground, frame, pose):
    phase = frame * 2 * math.pi / FPS
    walk = math.sin(phase * 1.4)
    bob = abs(math.sin(phase * 1.4)) * 5 if pose == "walk" else math.sin(phase) * 2
    head_y = int(ground - 255 - bob)
    cx = int(x)
    # Body and head remain identical across all scenes.
    draw.ellipse((cx - 43, head_y - 43, cx + 43, head_y + 43),
                 fill=(250, 250, 248), outline=(15, 17, 20), width=6)
    eye_y = head_y - 5
    draw.ellipse((cx - 16, eye_y, cx - 8, eye_y + 9), fill=(15, 17, 20))
    draw.ellipse((cx + 8, eye_y, cx + 16, eye_y + 9), fill=(15, 17, 20))
    draw.arc((cx - 14, head_y + 8, cx + 14, head_y + 29), 5, 175, fill=(15, 17, 20), width=3)

    shoulder = (cx, head_y + 48)
    hip = (cx, int(ground - 105 - bob))
    line(draw, [shoulder, hip], 8)

    if pose == "walk":
        arms = [(cx - 55, head_y + 105 + int(walk * 24)), (cx + 55, head_y + 105 - int(walk * 24))]
        legs = [(cx - 48 + int(walk * 35), ground), (cx + 48 - int(walk * 35), ground)]
    elif pose == "crouch":
        hip = (cx, ground - 135)
        arms = [(cx - 65, ground - 95), (cx + 55, ground - 125)]
        legs = [(cx - 55, ground - 5), (cx + 65, ground - 5)]
    elif pose in ("signal", "point"):
        arms = [(cx - 58, head_y + 125), (cx + 75, head_y - 5)]
        legs = [(cx - 38, ground), (cx + 38, ground)]
    elif pose == "sit":
        hip = (cx + 15, ground - 95)
        arms = [(cx - 55, head_y + 125), (cx + 55, head_y + 125)]
        legs = [(cx + 95, ground - 3), (cx + 145, ground - 3)]
    elif pose == "brace":
        arms = [(cx - 72, head_y + 90), (cx + 72, head_y + 90)]
        legs = [(cx - 55, ground), (cx + 55, ground)]
    else:
        arms = [(cx - 65, head_y + 125), (cx + 65, head_y + 125)]
        legs = [(cx - 45, ground), (cx + 45, ground)]

    line(draw, [shoulder, arms[0]], 7)
    line(draw, [shoulder, arms[1]], 7)
    line(draw, [hip, legs[0]], 8)
    line(draw, [hip, legs[1]], 8)

def draw_caption(draw, scene, index, total, topic):
    # Solid lower-third improves readability without hiding the action.
    draw.rectangle((0, 585, WIDTH, HEIGHT), fill=(18, 23, 30))
    draw.text((42, 600), f"{index + 1:02d} / {total:02d}", font=SMALL, fill=(160, 205, 220))
    draw.text((42, 628), scene["action"], font=FONT, fill=(250, 250, 248))
    draw.text((42, 680), topic[:100], font=SMALL, fill=(190, 200, 205))

def render_video(topic, scene_count, seconds_per_scene, filename):
    VIDEO_DIR.mkdir(exist_ok=True)
    output = VIDEO_DIR / filename
    scenes = make_scenes(topic, scene_count)
    frames_per_scene = seconds_per_scene * FPS

    with imageio.get_writer(str(output), fps=FPS, codec="libx264", quality=8,
                            macro_block_size=16) as writer:
        for scene_index, scene in enumerate(scenes):
            for frame in range(frames_per_scene):
                global_frame = scene_index * frames_per_scene + frame
                progress = frame / max(1, frames_per_scene - 1)
                # Slow camera drift and a small character position change
                # give each scene motion beyond limb oscillation.
                camera = scene_index * 22 + progress * 34
                img = Image.new("RGB", (WIDTH, HEIGHT), (180, 200, 210))
                draw = ImageDraw.Draw(img)
                draw_background(draw, topic, global_frame / FPS, camera)
                character_x = WIDTH * (0.50 + 0.045 * math.sin(progress * math.pi))
                draw_character(draw, character_x, GROUND_Y, global_frame, scene["pose"])
                draw_caption(draw, scene, scene_index, scene_count, topic)
                writer.append_data(np.asarray(img))

    print(f"VIDEO CREATED: {output}")
    return output

def main():
    random.seed()
    history = load_history()
    shorts_topic, long_topic = generate_topics(history)
    SCRIPT_DIR.mkdir(exist_ok=True)
    VIDEO_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    shorts_scenes = make_scenes(shorts_topic, 6)
    long_scenes = make_scenes(long_topic, 60)
    for filename, topic, scenes in [
        (f"shorts_{timestamp}.txt", shorts_topic, shorts_scenes),
        (f"long_{timestamp}.txt", long_topic, long_scenes),
    ]:
        body = "\n\n".join(
            f"SCENE {s['number']} — {s['beat'].upper()}\n"
            f"LOCATION: {s['location']}\nACTION: {s['action']}\n"
            f"POSE: {s['pose']}\nSTYLE: {STYLE}"
            for s in scenes
        )
        (SCRIPT_DIR / filename).write_text(f"TITLE: {topic}\n\n{body}", encoding="utf-8")

    render_video(shorts_topic, 6, 8, f"shorts_{timestamp}.mp4")
    render_video(long_topic, 60, 12, f"long_{timestamp}.mp4")

    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(shorts_topic + "\n" + long_topic + "\n")
    print("ALL VIDEOS CREATED!")

if __name__ == "__main__":
    main()
