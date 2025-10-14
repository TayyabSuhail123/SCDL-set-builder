import os
import subprocess
from typing import List
import re

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def download_track_audio(url: str, output_dir: str) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    info_cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(webpage_url)s",
        url
    ]
    try:
        info_result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        track_urls = [line.strip() for line in info_result.stdout.splitlines() if line.strip()]
    except Exception:
        track_urls = []
    file_paths = []
    output_template = os.path.join(output_dir, "%(title)s.mp3")
    if track_urls and len(track_urls) > 1:
        for track_url in track_urls:
            check_cmd = [
                "yt-dlp",
                "--get-title",
                track_url
            ]
            try:
                title_result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
                title = sanitize_filename(title_result.stdout.strip())
            except Exception:
                title = None
            output_path = os.path.join(output_dir, f"{title}.mp3") if title else None
            if output_path and os.path.isfile(output_path):
                print(f"Skipping (already exists): {output_path}")
                file_paths.append(output_path)
                continue
            print(f"Downloading: {track_url} -> {output_path}")
            cmd = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--output", output_template,
                track_url
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                if output_path and os.path.isfile(output_path):
                    file_paths.append(output_path)
            except Exception:
                print(f"Failed to download: {track_url}")
                continue
    else:
        check_cmd = [
            "yt-dlp",
            "--get-title",
            url
        ]
        try:
            title_result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
            title = sanitize_filename(title_result.stdout.strip())
        except Exception:
            title = None
        output_path = os.path.join(output_dir, f"{title}.mp3") if title else None
        if output_path and os.path.isfile(output_path):
            print(f"Skipping (already exists): {output_path}")
            file_paths.append(output_path)
        else:
            print(f"Downloading: {url} -> {output_path}")
            cmd = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--output", output_template,
                url
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                if output_path and os.path.isfile(output_path):
                    file_paths.append(output_path)
            except Exception:
                print(f"Failed to download: {url}")
                pass
    return file_paths
