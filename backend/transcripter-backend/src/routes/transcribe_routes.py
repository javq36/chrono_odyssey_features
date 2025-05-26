from flask import request, jsonify, Blueprint
import tempfile
import yt_dlp
from moviepy import VideoFileClip
import os
import glob
import openai
from pydub import AudioSegment

transcribe_bp = Blueprint('transcribe', __name__)

def download_youtube_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4/bestaudio/best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_title = info.get("title")
        channel_name = info.get("uploader")

def split_audio_to_chunks(audio_path, max_bytes=24*1024*1024):
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    start = 0
    duration_ms = len(audio)
    # Estimate bytes per ms
    bytes_per_ms = os.path.getsize(audio_path) / duration_ms
    chunk_duration_ms = int(max_bytes / bytes_per_ms)
    while start < duration_ms:
        end = min(start + chunk_duration_ms, duration_ms)
        chunk = audio[start:end]
        temp_chunk = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        chunk.export(temp_chunk.name, format="wav")
        chunks.append(temp_chunk.name)
        start = end
    return chunks

@transcribe_bp.route('/api/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, 'video.%(ext)s')
        download_youtube_video(video_url, output_path)
        video_files = glob.glob(os.path.join(temp_dir, 'video.*'))
        if not video_files:
            return jsonify({'error': 'Video download failed'}), 500
        temp_video_path = video_files[0]

        temp_audio_path = temp_video_path.replace('.mp4', '.wav')
        with VideoFileClip(temp_video_path) as video:
            video.audio.write_audiofile(temp_audio_path)

        # Split audio if too large
        audio_chunks = split_audio_to_chunks(temp_audio_path)
        transcript_text = ""
        for chunk_path in audio_chunks:
            with open(chunk_path, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                transcript_text += transcript.text + " "
            os.remove(chunk_path)

    return jsonify({'transcription': transcript_text.strip()})