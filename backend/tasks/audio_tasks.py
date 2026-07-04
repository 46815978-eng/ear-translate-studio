"""Edge-TTS 配音、ASMR混音、SRT字幕生成任务"""
import os
import asyncio
import json
from datetime import datetime
from celery import shared_task

from ..config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME


@shared_task(bind=True, max_retries=3)
def generate_tts_audio(self, text: str, language: str, output_path: str) -> dict:
    """
    使用 Edge-TTS 生成配音
    - text: 英文文本
    - language: en-US-JennyNeural / zh-CN-XiaoxiaoNeural
    - output_path: 输出音频文件路径
    """
    try:
        import edge_tts

        voice = "en-US-JennyNeural" if language.startswith("en") else "zh-CN-XiaoxiaoNeural"
        communicate = edge_tts.Communicate(text, voice)
        asyncio.run(communicate.save(output_path))

        return {
            "status": "success",
            "output": output_path,
            "language": language,
        }
    except ImportError:
        return {"status": "error", "message": "edge-tts 未安装"}
    except Exception as e:
        self.retry(exc=e, countdown=60)
        return {"status": "error", "message": str(e)}


@shared_task(bind=True, max_retries=3)
def mix_asmr_audio(self, audio_path: str, asmr_path: str, output_path: str) -> dict:
    """
    ASMR 混音：将配音与背景音混合，背景音音量 10%
    """
    try:
        import subprocess

        cmd = [
            'ffmpeg', '-y',
            '-i', audio_path,
            '-i', asmr_path,
            '-filter_complex',
            '[0:a]volume=1.0[a0];[1:a]volume=0.1[a1];[a0][a1]amix=inputs=2:duration=first[out]',
            '-map', '[out]',
            '-acodec', 'aac',
            '-ar', '44100',
            output_path,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return {"status": "success", "output": output_path}
    except subprocess.CalledProcessError as e:
        self.retry(exc=e, countdown=30)
        return {"status": "error", "message": str(e)}


@shared_task
def generate_srt_subtitles(text: str, duration_seconds: int) -> str:
    """
    从文本生成 SRT 双语字幕
    返回 SRT 格式字符串
    """
    # 按句号切分句子
    sentences = [s.strip() for s in text.replace('?', '.').replace('!', '.').split('.') if s.strip()]
    lines = []
    num_sentences = len(sentences)
    per_line = max(duration_seconds // max(num_sentences, 1), 3)

    for i, sentence in enumerate(sentences):
        idx = i + 1
        start = i * per_line
        end = (i + 1) * per_line
        h1, m1, s1 = start // 3600, (start % 3600) // 60, start % 60
        h2, m2, s2 = end // 3600, (end % 3600) // 60, end % 60
        lines.append(f"{idx}")
        lines.append(f"{h1:02d}:{m1:02d}:{s1:02d},000 --> {h2:02d}:{m2:02d}:{s2:02d},000")
        lines.append(sentence)
        lines.append("")

    return "\n".join(lines)
