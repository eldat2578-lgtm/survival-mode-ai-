import asyncio
import subprocess
import wave
from pathlib import Path
import numpy as np

def add_audio(video_path, narration, duration):
    video_path = Path(video_path)
    voice = video_path.with_suffix('.voice.mp3')
    music = video_path.with_suffix('.music.wav')
    temp = video_path.with_suffix('.mux.mp4')
    try:
        import edge_tts
        async def speak():
            job = edge_tts.Communicate(narration, 'en-US-GuyNeural', rate='+3%', volume='-8%')
            await job.save(str(voice))
        asyncio.run(speak())
        sr = 24000
        t = np.arange(int(sr * duration), dtype=np.float32) / sr
        bed = 0.035*np.sin(2*np.pi*110*t) + 0.018*np.sin(2*np.pi*164.81*t)
        bed *= 0.7 + 0.3*np.sin(2*np.pi*t/20)
        pcm = (np.clip(bed, -0.1, 0.1)*32767).astype(np.int16)
        with wave.open(str(music), 'wb') as out:
            out.setnchannels(1); out.setsampwidth(2); out.setframerate(sr); out.writeframes(pcm.tobytes())
        subprocess.run(['ffmpeg','-y','-i',str(video_path),'-i',str(voice),'-i',str(music),
          '-filter_complex','[1:a]volume=1.0[v];[2:a]volume=0.18[m];[v][m]amix=inputs=2:duration=longest[a]',
          '-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-shortest',str(temp)],
          check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        temp.replace(video_path)
        print('Narration and soundtrack added')
    except Exception as exc:
        print('Audio fallback: video retained without narration:', exc)
    finally:
        for p in (voice, music, temp):
            if p.exists(): p.unlink()
