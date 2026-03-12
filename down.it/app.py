from flask import Flask, request, render_template, redirect, url_for
import yt_dlp
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form.get('quality', 'bestaudio')
    music_dir = Path.home() / "Music"
    music_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': quality,
        'outtmpl': str(music_dir / '%(title)s.%(ext)s'),
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['title']}.{info['ext']}"
        return redirect(url_for('thank_you', filename=filename))
    except Exception as e:
        return f"<h3>Error:</h3><p>{str(e)}</p>"

@app.route('/thankyou')
def thank_you():
    filename = request.args.get('filename', 'Unknown File')
    return render_template('thankyou.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)