import logging
from flask import Flask, jsonify
from flask_cors import CORS

from reformat import reformat
from transcribe import transcribe_yt

app = Flask(__name__)
CORS(app)

audio_directory = 'audio'  # The directory where the audio files will be saved
app.config['DEBUG'] = False  # ensure this is False for production environment

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello World!'})

@app.route('/api/transcribe/<video_id>', methods=['GET'])
def transcribe(video_id):
    app.logger.info(f"Transcribing video with id: {video_id}")
    try:
        result = transcribe_yt(f'https://www.youtube.com/watch?v={video_id}')
        formatted = reformat(result['segments'])
        return jsonify({'script': formatted})
    except Exception as e:
        app.logger.error(f"Error transcribing video with id: {video_id}")
        app.logger.error(e)
        return jsonify({'error': 'Error processing request'}), 500

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO)
