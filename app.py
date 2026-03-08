import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich import print as rprint
from typing import Optional
import logic

app = typer.Typer(
    name="uvd",
    help="Universal Video Downloader — YouTube, Vimeo, Twitter/X, TikTok ve daha fazlasi.",
    add_completion=False,
)
console = Console()


def _make_progress_hook(progress, task_id):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                progress.update(task_id, completed=downloaded, total=total)
    return hook


@app.command()
def download(
    url: str = typer.Argument(..., help="Indirilecek video veya playlist URL'si"),
    output: str = typer.Option("downloads", "--output", "-o", help="Cikti klasoru"),
    quality: str = typer.Option(
        "best",
        "--quality", "-q",
        help="Video kalitesi: best, 1080p, 720p, 480p, audio",
        show_default=True,
    ),
    audio_only: bool = typer.Option(False, "--audio", "-a", help="Sadece ses indir (MP3)"),
    info_only: bool = typer.Option(False, "--info", "-i", help="Sadece bilgi goster, indirme"),
):
    """Verilen URL'deki videoyu veya playlist'i indirir."""

    # --- Bilgi alma ---
    console.print(f"\n[bold cyan]Bilgi aliyor...[/bold cyan] {url}")
    try:
        meta = logic.get_info(url)
    except Exception as e:
        console.print(f"[bold red]Hata:[/bold red] {e}")
        raise typer.Exit(1)

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("[dim]Baslik[/dim]",   f"[bold]{meta['title']}[/bold]")
    table.add_row("[dim]Kanal[/dim]",    meta["uploader"])
    table.add_row("[dim]Sure[/dim]",     logic.format_duration(meta["duration"]))
    table.add_row("[dim]Platform[/dim]", meta["extractor"])
    if meta["playlist"]:
        table.add_row("[dim]Playlist[/dim]", f"{meta['entry_count']} video")
    console.print(table)

    if info_only:
        return

    # --- Indirme ---
    if audio_only:
        if logic._ffmpeg_available():
            mode = "ses (MP3)"
        else:
            mode = "ses (ham format — MP3 icin ffmpeg kurun)"
    else:
        mode = f"video ({quality})"
    console.print(f"\n[bold green]Indiriliyor[/bold green] → [dim]{output}/[/dim]  [italic]{mode}[/italic]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("Indiriliyor...", total=None)
        hook = _make_progress_hook(progress, task_id)

        try:
            files = logic.download(
                url=url,
                output_dir=output,
                quality=quality,
                audio_only=audio_only,
                progress_hook=hook,
            )
        except Exception as e:
            console.print(f"\n[bold red]Indirme hatasi:[/bold red] {e}")
            raise typer.Exit(1)

        progress.update(task_id, completed=1, total=1, description="Tamamlandi")

    console.print("\n[bold green]Basariyla tamamlandi![/bold green]")
    for f in files:
        console.print(f"  [dim]→[/dim] {f}")
    console.print()


if __name__ == "__main__":
    app()
