window.onload = function() {
    if ('serviceWorker' in navigator) { // show other serviceworker in application tabs
        try {
            navigator.serviceWorker.register('/serviceworker.js');
            console.log('SW registered');
        } catch (error) {
            console.log('SW failed');

        }
    }
}

let prefixURL = 'http://13.127.65.157:5001'

let submit = document.getElementById('submit');
function sendURL() {
    let postURL = '?text=' + document.getElementById('url').value
    window.location.href = postURL
}
