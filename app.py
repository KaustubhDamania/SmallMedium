from flask import Flask, request, jsonify, render_template, url_for, send_from_directory, redirect
import json, requests
import os
import bs4
from requests.utils import requote_uri
import tweepy
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# with app.test_request_context():
#     print(url_for("static", filename="css/index.css"))


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
# ID of the recipient
# recipient_id = 1325417588344631299


def postRequest(url):
    res = requests.get(url)
    return res.json()

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
    # direct_message = api.send_direct_message(recipient_id, text)

    # printing the text of the sent direct message
    # print(direct_message)
    # print(direct_message.message_create)
    # print(direct_message.message_create['message_data']['text'])
    # twitter_url = direct_message.message_create['message_data']['text']
    tweet = api.update_status(text)
    print(tweet.text)
    twitter_url = tweet.text
    return redirect(twitter_url, code=302)
    # port = int(os.environ.get('PORT',5001))
    # prefixURL = 'http://127.0.0.1:5001' # post request url
    # postURL = prefixURL + '/crawl.json?spider_name=get_content&url='
    # postURL += requote_uri(text)
    print('Final URL is', postURL)
    # res = postRequest(postURL)
    # print(res)
    res = {
        'head': res['items'][0]['head'],
        'body': res['items'][0]['body']
    }
    return render_template('post.html', res=res)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('.', path)

if __name__=='__main__':
    app.run(debug=True)
