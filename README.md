# Universal Video Downloader

YouTube, Vimeo, Twitter/X, TikTok ve 1000+ platformdan video/ses indiren komut satiri araci.

## Kurulum

```bash
pip install -r requirements.txt
```

> **Not:** Ses donusturme icin sisteminizde `ffmpeg` kurulu olmasi gerekir.

## Kullanim

```bash
# En iyi kalitede indir
python app.py <URL>

# 720p indir, belirli klasore
python app.py <URL> --quality 720p --output ./videolar

# Sadece ses (MP3) indir
python app.py <URL> --audio

# Bilgi goster, indirme
python app.py <URL> --info
```

## Secenekler

| Secenek | Kisayol | Varsayilan | Aciklama |
|---------|---------|------------|----------|
| `--output` | `-o` | `downloads` | Cikti klasoru |
| `--quality` | `-q` | `best` | `best`, `1080p`, `720p`, `480p`, `audio` |
| `--audio` | `-a` | `False` | Sadece MP3 indir |
| `--info` | `-i` | `False` | Sadece bilgi goster |

## Dosya Yapisi

```
.
├── app.py          # CLI arayuzu (Typer + Rich)
├── logic.py        # Cekirdek indirme mantigi (yt-dlp)
└── requirements.txt
```
