import json
from os import environ

import requests
from flask import Flask, render_template, request
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import isodate

app = Flask(__name__)

load_dotenv()


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code
    if request.method == 'GET':
        return render_template('home.html', test="Elie Pernet")
    else:
        url = request.form.get('url')
        if url:
            url = urlparse(url)
            video_id = parse_qs(url.query).get('v')[0]

            if video_id:
                req = requests.get(f'https://www.googleapis.com/youtube/v3/videos'
                                   f'?id={video_id}'
                                   f'&key={environ.get("YOUTUBE_API_KEY")}'
                                   f'&part=snippet,contentDetails,statistics,status')
                video_info = dict(req.json()).get('items')[0]
                video_thumbnail = video_info['snippet']['thumbnails']['medium']['url']
                video_title = video_info['snippet']['title']
                video_duration = video_info['contentDetails']['duration']
                duration_parser = isodate.parse_duration(video_duration)
                video_duration = f'{duration_parser.seconds // 60}:{duration_parser.seconds % 60}'

                return f'''
                    <div class="card">
                        <div class="card__image-container">
                            <img class="card__image" src="{video_thumbnail}"/>
                            <p class="card__duration">{video_duration}</p>
                        </div>
                        <h3 class="card__title">{video_title}</h3>
                    </div>
                '''


if __name__ == '__main__':
    app.run()
