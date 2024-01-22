from flask import Flask, render_template, send_file
from flask_cors import CORS, cross_origin
from requests import get
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/img/<image>')
def images(image):
    return send_file(f'./templates/{image}')

@app.route('/api/<username>')
@cross_origin()
def current(username):
    r = get(f'https://www.last.fm/user/{username}').content

    html = BeautifulSoup(r, 'html.parser').find('tr', attrs={'class': 'chartlist-row'})

    image = html.find('img').get('src')
    name = html.find('td', attrs={'class', 'chartlist-name'}).text.replace('\n', '')
    artist = html.find('td', attrs={'class', 'chartlist-artist'}).text.replace('\n', '')

    return {
        'status': True,
        'name': name,
        'artist': artist,
        'cover': image
    }

app.run(port=4000, debug=True)