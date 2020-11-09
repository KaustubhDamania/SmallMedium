from flask import Flask, request, jsonify, render_template, url_for, send_from_directory, redirect
import json, requests
import os
import bs4
from requests.utils import requote_uri
import tweepy
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# assign the values accordingly
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
api.verify_credentials()

def get_original_url(url):
    if 'link.medium' not in url:
        return url
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    meta_tags = soup.find_all('meta')
    for meta_tag in meta_tags:
        if meta_tag.get('property') == 'og:url':
            return meta_tag.get('content')

@app.route('/', methods=['GET'])
def home():
    text = request.args.get('text')
    if not text:
        return render_template('index.html')
    text = text.split()
    print(text)
    text = text[-1]
    print(text)
    text = get_original_url(text)
    tweet = api.update_status(text)
    print(tweet.text)
    twitter_url = tweet.text
    return redirect(twitter_url, code=302)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('.', path)

if __name__=='__main__':
    app.run(debug=True)
