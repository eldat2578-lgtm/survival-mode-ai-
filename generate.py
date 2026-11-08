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
WIDTH, HEIGHT, SCALE, FPS = 1280, 720, 2, 12
W, H = WIDTH * SCALE, HEIGHT * SCALE

PLACES = ["a deserted island", "an abandoned city", "a dense forest", "the Arctic",
          "a remote desert", "a snowy mountain", "an empty underground station", "a remote village"]
SITUATIONS = ["What If You Got Stranded in", "What If You Woke Up Alone in",
              "How Would You Survive in", "Could You Survive in"]
CHALLENGES = ["with No Food or Water?", "During a Massive Storm?", "Without Electricity?",
              "During the Coldest Night?", "With No Way to Contact Anyone?"]

def load_history():
    return set(HISTORY_FILE.read_text(encoding="utf-8").splitlines()) if HISTORY_FILE.exists() else set()

def generate_topics(history):
    options = [f"{s} {p} {c}" for s in SITUATIONS for p in PLACES for c in CHALLENGES]
    available = [topic for topic in options if topic not in history]
    if len(available) < 2:
        raise RuntimeError("Not enough unused topics")
    return random.sample(available, 2)

def make_scenes(topic, count):
    beats = [
        "A sudden discovery changes everything.",
        "The survivor studies the unfamiliar landscape.",
        "A distant sound interrupts the silence.",
        "The survivor finds a possible route to safety.",
        "A new obstacle appears in the distance.",
        "The survivor makes a careful plan."
    ]
    return [f"SCENE {i + 1}\nLOCATION: {topic}\nACTION: {beats[(i - 1) % len(beats)]}\n"
            for i in range(1, count + 1)]

def S(v):
    return int(v * SCALE)

def font(size, bold=False):
    candidates = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
                  ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    try:
        return ImageFont.truetype(candidates[0], S(size))
    except OSError:
        return ImageFont.load_default()

def gradient(draw):
    top, bottom = (22, 42, 72), (238, 180, 112)
    for y in range(H):
        t = y / max(1, H - 1)
        col = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line((0, y, W, y), fill=col)

def polygon(draw, points, fill, outline=None, width=1):
    pts = [(S(x), S(y)) for x, y in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=S(width), joint="curve")

def background(topic, frame, scene_index):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    gradient(d)
    drift = (frame * 0.45 + scene_index * 23) % 160
    # distant clouds and warm atmospheric sun
    d.ellipse((S(960 - drift * .2), S(72), S(1100 - drift * .2), S(212)), fill=(255, 218, 155))
    for cx, cy, r in [(180, 150, 34), (410, 210, 24), (790, 125, 30)]:
        x = S((cx - drift * .35) % 1450 - 80)
        d.ellipse((x, S(cy), x + S(r * 2), S(cy + r)), fill=(255, 232, 208))
        d.ellipse((x + S(18), S(cy - 18), x + S(r * 2 - 5), S(cy + r)), fill=(255, 232, 208))
    if "forest" in topic:
        polygon(d, [(0,470),(180,280),(350,470),(560,250),(780,470),(1000,290),(1280,470)], (49,91,82))
        for x in range(-100, 1450, 175):
            xx = x - int(drift * .8) % 175
            d.rectangle((S(xx+65),S(315),S(xx+90),S(570)), fill=(69,48,43))
            polygon(d, [(xx,365),(xx+78,190),(xx+155,365)], (38,103,78))
            polygon(d, [(xx+12,300),(xx+78,145),(xx+143,300)], (48,125,87))
        ground=(55,105,75)
    elif "city" in topic or "station" in topic:
        for x in range(-80, 1400, 190):
            xx=x-int(drift*.55)%190
            h=190+(x%3)*45
            d.rectangle((S(xx),S(475-h),S(xx+145),S(500)), fill=(48,65,83))
            d.rectangle((S(xx+9),S(485-h),S(xx+136),S(490)), fill=(75,91,108))
            for wy in range(500-h+28,490,48):
                for wx in (xx+24,xx+78):
                    d.rounded_rectangle((S(wx),S(wy),S(wx+25),S(wy+27)),radius=S(4),fill=(238,190,125))
        ground=(54,65,76)
    elif "Arctic" in topic or "snowy" in topic:
        polygon(d,[(0,490),(250,210),(490,490),(800,145),(1120,490),(1280,360),(1280,720),(0,720)],(194,214,224))
        polygon(d,[(250,210),(330,300),(290,285),(250,340),(205,300)],(245,248,248))
        polygon(d,[(800,145),(900,260),(850,240),(800,305),(750,260)],(248,250,250))
        ground=(225,235,239)
    elif "desert" in topic:
        polygon(d,[(0,470),(260,330),(570,490),(900,315),(1280,470),(1280,720),(0,720)],(181,126,83))
        polygon(d,[(0,540),(350,420),(720,560),(1080,405),(1280,490),(1280,720),(0,720)],(213,158,99))
        ground=(213,158,99)
    elif "island" in topic:
        d.rectangle((0,S(470),W,H),fill=(43,133,157))
        for y in range(500,720,42):
            d.arc((S(0),S(y),W,S(y+38)),0,180,fill=(111,196,194),width=S(3))
        polygon(d,[(120,520),(250,390),(500,420),(730,520)],(226,192,133))
        ground=(226,192,133)
    else:
        polygon(d,[(0,470),(240,330),(500,470),(830,300),(1280,470),(1280,720),(0,720)],(91,112,100))
        ground=(105,119,94)
    d.rectangle((0,S(540),W,H),fill=ground)
    # foreground depth silhouettes
    for x in range(-50,1400,260):
        xx=x-int(drift*1.35)%260
        d.ellipse((S(xx),S(570+(x%4)*9),S(xx+190),S(635+(x%4)*9)),fill=tuple(max(0,c-12) for c in ground))
    return im

def character(im, frame, scene_index):
    d=ImageDraw.Draw(im)
    walk=math.sin(frame*.34)
    bob=math.sin(frame*.68)*5
    x=640+int(math.sin(frame*.035+scene_index)*18)
    y=355+int(bob)
    ink=(20,24,31)
    # soft ground shadow
    d.ellipse((S(x-90),S(637),S(x+90),S(660)),fill=(35,39,42))
    # legs with alternating stride
    hip=(x,y+180)
    d.line((S(*hip),S(x-45+walk*35),S(300)),fill=ink,width=S(13))
    d.line((S(x,y+180),S(x+45-walk*35),S(300)),fill=ink,width=S(13))
    # torso and arms
    d.line((S(x),S(y+48),S(x),S(y+185)),fill=ink,width=S(15))
    d.line((S(x),S(y+85),S(x-70-walk*20),S(y+145+walk*16)),fill=ink,width=S(12))
    d.line((S(x),S(y+85),S(x+70+walk*20),S(y+145-walk*16)),fill=ink,width=S(12))
    # white head with thick clean outline
    d.ellipse((S(x-61),S(y-65),S(x+61),S(y+57)),fill=(250,250,247),outline=ink,width=S(8))
    blink=(frame%83 in (0,1))
    if blink:
        d.line((S(x-27),S(y-12),S(x-12),S(y-12)),fill=ink,width=S(5))
        d.line((S(x+12),S(y-12),S(x+27),S(y-12)),fill=ink,width=S(5))
    else:
        d.ellipse((S(x-25),S(y-19),S(x-13),S(y-3)),fill=ink)
        d.ellipse((S(x+13),S(y-19),S(x+25),S(y-3)),fill=ink)
    d.arc((S(x-22),S(y+1),S(x+22),S(y+34)),10,165,fill=ink,width=S(4))

def render_video(topic, scene_count, seconds_per_scene, filename):
    VIDEO_DIR.mkdir(exist_ok=True)
    output=VIDEO_DIR/filename
    scenes=make_scenes(topic,scene_count)
    with imageio.get_writer(str(output),fps=FPS,codec="libx264",quality=7,macro_block_size=16) as writer:
        for si,scene in enumerate(scenes):
            action=scene.split("ACTION: ")[1].strip()
            for frame in range(seconds_per_scene*FPS):
                im=background(topic,frame,si)
                character(im,frame,si)
                d=ImageDraw.Draw(im)
                # cinematic lower-third panel
                d.rounded_rectangle((S(38),S(574),S(1242),S(694)),radius=S(22),fill=(12,19,29))
                d.rounded_rectangle((S(55),S(590),S(63),S(675)),radius=S(4),fill=(255,181,91))
                d.text((S(84),S(588)),f"{si+1:02d} / {scene_count:02d}",font=font(17,True),fill=(255,190,112))
                d.text((S(84),S(622)),action,font=font(23,True),fill=(250,250,247))
                # progress indicator
                progress=(si+frame/(seconds_per_scene*FPS))/scene_count
                d.rounded_rectangle((S(40),S(706),S(1240),S(712)),radius=S(3),fill=(75,82,91))
                d.rounded_rectangle((S(40),S(706),S(40+1200*progress),S(712)),radius=S(3),fill=(255,181,91))
                # antialias downsample
                im=im.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
                writer.append_data(np.asarray(im))
    print("VIDEO CREATED:",output)
    return output

def main():
    random.seed()
    history=load_history()
    shorts_topic,long_topic=generate_topics(history)
    SCRIPT_DIR.mkdir(exist_ok=True)
    timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shorts_scenes=make_scenes(shorts_topic,6)
    long_scenes=make_scenes(long_topic,60)
    (SCRIPT_DIR/f"shorts_{timestamp}.txt").write_text(f"TITLE: {shorts_topic}\n\n"+"\n".join(shorts_scenes),encoding="utf-8")
    (SCRIPT_DIR/f"long_{timestamp}.txt").write_text(f"TITLE: {long_topic}\n\n"+"\n".join(long_scenes),encoding="utf-8")
    render_video(shorts_topic,6,8,f"shorts_{timestamp}.mp4")
    render_video(long_topic,60,12,f"long_{timestamp}.mp4")
    with HISTORY_FILE.open("a",encoding="utf-8") as f:
        f.write(shorts_topic+"\n"+long_topic+"\n")
    print("ALL VIDEOS CREATED!")

if __name__=="__main__":
    main()
