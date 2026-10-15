import os
from celery import Celery
import yt_dlp

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("ytm_worker", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    timezone="UTC",
)

@celery_app.task(bind=True, name="tasks.download_media")
def download_media(self, video_id: str, mode: str= "audio"):
    """
    Background worker job to fetch high-fidelity audio or video tracks.
    Utilises FFmpeg inside the docker environment to handle post-muxing/encoding
    """
    url= f"https://youtube.com{video_id}"

    output_dir = f"/app/downloads/{mode}"
    os.makedirs(output_dir,exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    def yt_dlp_hook(d):
        if d["status"] == "downloading":
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total) * 100 if total > 0 else 0

            self.update_state(
                state="PROGRESS",
                meta={"percent": round(percent, 2), "downloaded": downloaded, "total": total}
            )

        if mode == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'error',
                'source_address': '0.0.0.0',
                'prefer_ffmpeg': True,
                'progress_hooks': [yt_dlp_hook],
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '256'
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'error',
                'source_address': '0.0.0.0',
                'prefer_ffmpeg': True,
                'progress_hooks': [yt_dlp_hook],
                'outtmpl': output_template,
                'merge_output_format': 'mp4'
            }
        try:
            self.update_state(state="PROGRESS", meta={"percent":0, "status": "Initializing stream hooks"})
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if mode == "audio":
                    filename = os.path.splitext(filename)[0] + ".mp3"
                    return {
                        "status": "COMPLETED",
                        "title": info.get("title"),
                        "file_path": filename,
                        "mode": mode

                    }
        except Exception as e:
            self.update_state(state="FAILURE", meta={"error": str(e)})
            raise e