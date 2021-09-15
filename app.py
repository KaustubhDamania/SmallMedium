from flask import Flask, request, jsonify, render_template, url_for, send_from_directory, redirect
import json, requests
import os
import bs4
from urllib.parse import urlsplit, urlunsplit
from requests.utils import requote_uri
import tweepy
import psycopg2
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# assign the values accordingly
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
database_url = os.getenv('DATABASE_URL')

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
api.verify_credentials()

# conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres')
conn = psycopg2.connect(database_url, sslmode='require')

cursor = conn.cursor()

GET_TWITTER_URL_QUERY = 'select twitter_url from medium_to_twitter_urls where medium_url=%s;'
PUT_TWITTER_URL_QUERY = 'insert into medium_to_twitter_urls values (%s, %s);'

def get_twitter_url_from_db(medium_url):
    print('In get_twitter_url_from_db({})'.format(medium_url))
    try:
        cursor.execute(GET_TWITTER_URL_QUERY, (medium_url,))
        row = cursor.fetchone()
        if not row:
            return None
        return row[0]
    except Exception as e:
        conn.rollback()
        print('Exception occured while select query', e)

def put_twitter_url_in_db(medium_url, twitter_url):
    print('In put_twitter_url_in_db({}, {})'.format(medium_url, twitter_url))
    try:
        cursor.execute(PUT_TWITTER_URL_QUERY, (medium_url, twitter_url))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('Exception occured while insert query', e)


def remove_query_params(url):
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))

def get_original_url(url):
    response = requests.head(url)
    result = response.headers.get('Location')
    if not result:
        return url
    return remove_query_params(result)

def get_twitter_url(medium_url):
    if 'link.medium' in medium_url:
        fetched_twitter_url = get_twitter_url_from_db(medium_url)
        if fetched_twitter_url: # found in db, no need of tweeting it again
            return fetched_twitter_url
        full_medium_url = get_original_url(medium_url)
    else:
        full_medium_url = medium_url

    fetched_twitter_url = get_twitter_url_from_db(full_medium_url)
    if fetched_twitter_url: # found in db, no need of tweeting it again
        put_twitter_url_in_db(medium_url, fetched_twitter_url)
        return fetched_twitter_url

    # full_medium_url would be of form :- https://hostname.com/article instead
    # of https://link.medium.com/article

    tweet = api.update_status(full_medium_url)
    twitter_url = tweet.text

    # twitter_url = 'https://t.co/QNGoQzU3eO'

    put_twitter_url_in_db(full_medium_url, twitter_url)
    if full_medium_url != medium_url: # put link.medium.com url too in DB
        put_twitter_url_in_db(medium_url, twitter_url)
    return twitter_url

@app.route('/', methods=['GET'])
def home():
    medium_url = request.args.get('text')
    # print(medium_url)
    if not medium_url:
        return render_template('index.html')
    # medium_url = medium_url.split()
    # print(medium_url)
    # medium_url = medium_url[-1]
    print(medium_url)
    twitter_url = get_twitter_url(medium_url)
    print('Got twitter_url', twitter_url)
    return redirect(twitter_url, code=302)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('.', path)

if __name__=='__main__':
    app.run(debug=True)
