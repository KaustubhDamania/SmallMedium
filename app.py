from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
import json, requests
import os
import bs4
from requests.utils import requote_uri

app = Flask(__name__)
# with app.test_request_context():
#     print(url_for("static", filename="css/index.css"))


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
    port = int(os.environ.get('PORT',5001))
    prefixURL = 'http://54.196.8.61:5001' # post request url
    postURL = prefixURL + '/crawl.json?spider_name=get_content&url='
    text = get_original_url(text)
    postURL += requote_uri(text)
    print('Final URL is', postURL)
    res = postRequest(postURL)
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
