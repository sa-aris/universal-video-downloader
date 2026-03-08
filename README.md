# Universal Video Downloader

A command-line tool to download videos and audio from YouTube, Vimeo, Twitter/X, TikTok, and 1000+ platforms.

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** `ffmpeg` must be installed on your system for audio conversion (MP3) and video stream merging.

## Usage

```bash
# Download at best available quality
python3 app.py <URL>

# Download at 720p to a specific folder
python3 app.py <URL> --quality 720p --output ./videos

# Download audio only (MP3)
python3 app.py <URL> --audio

# Show info without downloading
python3 app.py <URL> --info
```

## Options

| Option | Shorthand | Default | Description |
|--------|-----------|---------|-------------|
| `--output` | `-o` | `downloads` | Output directory |
| `--quality` | `-q` | `best` | Quality: `best`, `1080p`, `720p`, `480p` |
| `--audio` | `-a` | `False` | Download audio only (MP3) |
| `--info` | `-i` | `False` | Show video info without downloading |

## Web Interface (Mobile & Desktop)

Start the web server:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in any browser — works on mobile too if both devices are on the same network.

## File Structure

```
.
├── app.py           # CLI interface (Typer + Rich)
├── server.py        # Web server (FastAPI)
├── logic.py         # Core download logic (yt-dlp)
├── static/
│   └── index.html   # Web UI
└── requirements.txt
```
