import yt_dlp
import os
from pathlib import Path


QUALITY_FORMATS = {
    "best": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "audio": "bestaudio/best",
}


def build_ydl_opts(output_dir: str, quality: str, audio_only: bool) -> dict:
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    fmt = "bestaudio/best" if audio_only else QUALITY_FORMATS.get(quality, QUALITY_FORMATS["best"])

    postprocessors = []
    if audio_only:
        postprocessors.append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        })

    return {
        "format": fmt,
        "outtmpl": str(out_path / "%(title)s.%(ext)s"),
        "noplaylist": False,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": postprocessors,
    }


def get_info(url: str) -> dict:
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "Unknown"),
            "uploader": info.get("uploader", "Unknown"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "extractor": info.get("extractor_key", "Unknown"),
            "playlist": info.get("_type") == "playlist",
            "entry_count": len(info.get("entries", [])) if info.get("_type") == "playlist" else 1,
        }


def download(
    url: str,
    output_dir: str = "downloads",
    quality: str = "best",
    audio_only: bool = False,
    progress_hook=None,
) -> list[str]:
    opts = build_ydl_opts(output_dir, quality, audio_only)

    downloaded_files = []

    def _default_hook(d):
        if d["status"] == "finished":
            downloaded_files.append(d["filename"])
        if progress_hook:
            progress_hook(d)

    opts["progress_hooks"] = [_default_hook]

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    # yt-dlp may rename files after postprocessing; scan output dir for result
    if not downloaded_files:
        out_path = Path(output_dir)
        downloaded_files = [str(f) for f in out_path.iterdir() if f.is_file()]

    return downloaded_files


def format_duration(seconds: int | None) -> str:
    if seconds is None:
        return "unknown"
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
