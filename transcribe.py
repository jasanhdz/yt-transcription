import whisper
import os
import hashlib
from pytube import YouTube

model_name = "tiny.en"  # Whisper model to use
model = whisper.load_model(model_name)


def download_video(url):
    yt = YouTube(url)
    hash_file = hashlib.md5()
    print('Downloading video...')
    hash_file.update(yt.title.encode())
    file_name = f'{hash_file.hexdigest()}.mp4'
    print(f'Saving video as {file_name}')
    yt.streams.first().download("", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }


def transcribe_yt(url):
    video = download_video(url)
    print('Transcribing video...')
    result = model.transcribe(video["file_name"])
    print('Transcription complete!')
    os.remove(video["file_name"])

    segments = []
    for item in result["segments"]:
        segments.append(format_item(item))

    return {
        "title": video["title"],
        "segments": segments
    }


def format_item(item):
    return {
        "time": item["start"],
        "text": item["text"]
    }