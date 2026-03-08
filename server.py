import os
import uuid
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import logic

app = FastAPI(title="Universal Video Downloader")
app.mount("/static", StaticFiles(directory="static"), name="static")


class InfoRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    quality: str = "best"
    audio_only: bool = False


def cleanup(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


@app.get("/", response_class=HTMLResponse)
def index():
    return Path("static/index.html").read_text()


@app.post("/info")
def get_info(req: InfoRequest):
    try:
        return logic.get_info(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download")
def download(req: DownloadRequest, background_tasks: BackgroundTasks):
    tmp_dir = os.path.join(tempfile.gettempdir(), f"uvd_{uuid.uuid4().hex}")

    try:
        files = logic.download(
            url=req.url,
            output_dir=tmp_dir,
            quality=req.quality,
            audio_only=req.audio_only,
        )
    except Exception as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

    if not files:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail="Download failed: no output file.")

    file_path = files[-1]
    filename = Path(file_path).name

    background_tasks.add_task(cleanup, tmp_dir)

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )
