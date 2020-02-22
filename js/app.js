if ('serviceWorker' in navigator) { // show other serviceworker in application tabs
    try {
        navigator.serviceWorker.register('../serviceworker.js');
        console.log('SW registered');
    } catch (error) {
        console.log('SW failed');

    }
}

window.addEventListener('load', () => {
    const parsedUrl = new URL(window.location);
    // searchParams.get() will properly handle decoding the values.
    let title = parsedUrl.searchParams.get('text');
    if (title==null) {
        return;
    }
    console.log('Title shared: ' + title);
    title = title.split(' ');
    title = title[title.length-1];
    let slashIndex = window.location.href.lastIndexOf('/')
    let prefixURL = window.location.href.slice(0,slashIndex)
    prefixURL = prefixURL.replace('5000','5001')
    let postURL = prefixURL + '/crawl.json?spider_name=get_content&url='
    postURL += encodeURIComponent(title)
    console.log('Final URL is', postURL);
    postRequest(postURL);
});

function postRequest(url){
    fetch(url, {
        'method': 'GET'
    })
    .then(res => res.json())
    .then(json => {
        console.log(json);
        document.getElementsByTagName('head')[0].innerHTML += json.items[0].head
        document.getElementsByClassName('container')[0].innerHTML = json.items[0].body
        document.getElementsByClassName('container')[0].style = "margin-bottom: 50px;"

    })
    .catch(err => console.log(err));
}

let submit = document.getElementById('submit');
function sendURL() {
    let slashIndex = window.location.href.lastIndexOf('/')
    let prefixURL = window.location.href.slice(0,slashIndex)
    prefixURL = prefixURL.replace('5000','5001')
    console.log(prefixURL);
    let postURL = prefixURL + '/crawl.json?spider_name=get_content&url='
    let articleURL = document.getElementById('url').value
    postURL += encodeURIComponent(articleURL)
    console.log('Final POST url',postURL);
    postRequest(postURL);
}
