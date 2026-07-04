#!/usr/bin/env python3
"""
哇学社 视频渲染工具
使用 FFmpeg 渲染 16:9 纯黑底短视频 + 双语字幕 + ASMR 背景音

用法:
    python ffmpeg_render.py --srt subtitles.srt --audio speech.wav --bg_audio asmr.wav --output result.mp4
"""
import subprocess
import argparse
import os
import sys


def render_video(srt_file, audio_file, bg_audio_file, output_file,
                 bg_color="black", width=1920, height=1080, bg_vol=10):
    """
    两步渲染：
    1. 纯色背景 + SRT字幕 + 主音频 → 临时文件
    2. 混入ASMR背景音 → 最终输出
    """
    for f, name in [(srt_file, "字幕"), (audio_file, "音频"), (bg_audio_file, "背景音")]:
        if not os.path.exists(f):
            print(f"[ERROR] {name}文件不存在: {f}")
            sys.exit(1)

    # 切换到输入文件所在目录（避免路径转义问题）
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    orig_cwd = os.getcwd()
    os.chdir(project_dir)

    # 使用相对路径（避免Windows路径转义）
    srt_rel = os.path.relpath(srt_file, project_dir)
    audio_rel = os.path.relpath(audio_file, project_dir)
    bg_rel = os.path.relpath(bg_audio_file, project_dir)
    output_rel = os.path.relpath(output_file, project_dir)
    temp_rel = output_rel + ".temp.mp4"

    try:
        print(f"[FFmpeg] 开始渲染...")
        print(f"  背景色: {bg_color}")
        print(f"  分辨率: {width}x{height}")
        print(f"  字幕: {srt_rel}")
        print(f"  主音: {audio_rel}")
        print(f"  背景音音量: {bg_vol}%")

        # Step 1: 渲染字幕视频
        cmd1 = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', f'color=c={bg_color}:s={width}x{height}:r=30',
            '-i', audio_rel,
            '-filter_complex',
            f"[0:v]subtitles='{srt_rel}':force_style="
            f"'FontName=Arial,FontSize=36,PrimaryColour=&H00FFFFFF,"
            f"OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=80'[v]",
            '-map', '[v]', '-map', '1:a',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-ar', '44100', '-b:a', '192k',
            '-shortest', temp_rel,
        ]
        result = subprocess.run(cmd1, capture_output=True, text=True, timeout=1800)
        if result.returncode != 0:
            print(f"[ERROR] Step 1 失败 (rc={result.returncode})")
            print(f"  STDERR: {result.stderr[-500:]}")
            sys.exit(1)
        print(f"  Step 1 OK: 字幕视频已生成")

        # Step 2: 混入ASMR背景音
        cmd2 = [
            'ffmpeg', '-y',
            '-i', temp_rel,
            '-i', bg_rel,
            '-filter_complex',
            f'[1:a]volume={bg_vol/100}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]',
            '-map', '0:v', '-map', '[aout]',
            '-c:v', 'copy', '-c:a', 'aac', '-ar', '44100', '-b:a', '192k',
            output_rel,
        ]
        result = subprocess.run(cmd2, capture_output=True, text=True, timeout=1800)
        if result.returncode != 0:
            print(f"[ERROR] Step 2 失败 (rc={result.returncode})")
            print(f"  STDERR: {result.stderr[-500:]}")
            sys.exit(1)

        if os.path.exists(output_rel):
            size_mb = os.path.getsize(output_rel) / 1024 / 1024
            print(f"[OK] 视频渲染完成: {output_file} ({size_mb:.1f} MB)")
        else:
            print(f"[ERROR] 输出文件未生成")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("[ERROR] FFmpeg 超时（>30分钟）")
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] 未找到 FFmpeg，请确保已安装并加入 PATH")
        sys.exit(1)
    finally:
        os.chdir(orig_cwd)
        if os.path.exists(temp_rel):
            os.remove(temp_rel)


def main():
    parser = argparse.ArgumentParser(description="哇学社视频渲染工具")
    parser.add_argument('--srt', required=True, help='SRT字幕文件')
    parser.add_argument('--audio', required=True, help='配音音频文件')
    parser.add_argument('--bg_audio', required=True, help='ASMR背景音频')
    parser.add_argument('--output', required=True, help='输出MP4文件')
    parser.add_argument('--bg_color', default='black', help='背景色')
    parser.add_argument('--width', type=int, default=1920, help='视频宽度')
    parser.add_argument('--height', type=int, default=1080, help='视频高度')
    parser.add_argument('--bg_vol', type=int, default=10, help='背景音量百分比')
    args = parser.parse_args()

    render_video(
        srt_file=args.srt,
        audio_file=args.audio,
        bg_audio_file=args.bg_audio,
        output_file=args.output,
        bg_color=args.bg_color,
        width=args.width,
        height=args.height,
        bg_vol=args.bg_vol,
    )


if __name__ == '__main__':
    main()
