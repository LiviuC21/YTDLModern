import os
import re
import yt_dlp
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadWorker(QThread):
    progress_updated = pyqtSignal(float, str, str, str)
    download_finished = pyqtSignal(bool, str)

    def __init__(self, url: str, output_path: str, format_type: str, noplaylist: bool = True):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.format_type = format_type
        self.noplaylist = noplaylist
        self._is_cancelled = False

    def stop(self):
        self._is_cancelled = True

    def run(self):
        ydl_opts = {
            'progress_hooks': [self._progress_hook],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'nocolors': True,  # Add this option to avoid ANSI color escape sequences
            'noplaylist': self.noplaylist
        }

        if self.format_type == 'MP4':
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
        elif self.format_type == 'MP3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        else:
            self.download_finished.emit(False, "Invalid format type")
            return

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.download_finished.emit(True, "Download completed successfully")
        except Exception as e:
            self.download_finished.emit(False, str(e))

    def _progress_hook(self, d):
        if self._is_cancelled:
            raise Exception('Descărcarea a fost oprită de utilizator.')

        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%')
            percent_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).strip()
            try:
                percent = float(percent_str.replace('%', ''))
            except ValueError:
                percent = 0.0

            speed = str(d.get('_speed_str') or 'N/A')
            eta = str(d.get('_eta_str') or 'N/A')
            status = d['status']
            self.progress_updated.emit(percent, speed, eta, status)
        elif d['status'] == 'finished':
            self.progress_updated.emit(100.0, "0B/s", "00:00", "finished")
