import asyncio
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np


def _make_music(path: Path, duration: float) -> None:
    sample_rate = 24000
    t = np.arange(int(sample_rate * duration), dtype=np.float32) / sample_rate
    # A quiet, slow ambient bed; no abrupt percussion.
    bed = (
        0.030 * np.sin(2 * np.pi * 110.0 * t)
        + 0.016 * np.sin(2 * np.pi * 164.81 * t)
        + 0.008 * np.sin(2 * np.pi * 220.0 * t)
    )
    bed *= 0.72 + 0.28 * np.sin(2 * np.pi * t / 24.0)
    pcm = (np.clip(bed, -0.12, 0.12) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sample_rate)
        out.writeframes(pcm.tobytes())


def _make_voice(path: Path, narration: str) -> bool:
    try:
        import edge_tts

        async def speak():
            job = edge_tts.Communicate(
                narration, "en-US-GuyNeural", rate="+3%", volume="-8%"
            )
            await job.save(str(path))

        asyncio.run(speak())
        return path.exists() and path.stat().st_size > 1000
    except Exception as exc:
        print("Narration unavailable; using music only:", exc)
        return False


def add_audio(video_path, narration, duration):
    video_path = Path(video_path)
    voice = video_path.with_suffix(".voice.mp3")
    music = video_path.with_suffix(".music.wav")
    temp = video_path.with_suffix(".mux.mp4")
    try:
        _make_music(music, duration)
        has_voice = _make_voice(voice, narration)
        inputs = ["-i", str(video_path)]
        if has_voice:
            inputs += ["-i", str(voice)]
        inputs += ["-i", str(music)]

        if has_voice:
            filter_graph = (
                "[1:a]volume=1.0[v];"
                "[2:a]volume=0.20[m];"
                "[v][m]amix=inputs=2:duration=longest[a]"
            )
            audio_map = "[a]"
        else:
            filter_graph = "[1:a]volume=0.22[a]"
            audio_map = "[a]"

        command = [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", filter_graph,
            "-map", "0:v:0", "-map", audio_map,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
            "-shortest", str(temp),
        ]
        subprocess.run(
            command, check=True, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, text=True
        )
        if not temp.exists() or temp.stat().st_size < 10000:
            raise RuntimeError("Audio mux produced an invalid output file")
        temp.replace(video_path)
        print("Audio track added:", "voice + music" if has_voice else "music only")
    except Exception as exc:
        print("Audio mux failed; original video retained:", exc)
    finally:
        for path in (voice, music, temp):
            if path.exists():
                path.unlink()
