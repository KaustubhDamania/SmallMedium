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

let form = document.getElementById('form');

form.addEventListener('submit',sendURL);

function sendURL(e) {
    e.preventDefault();
    let postURL = '?text=' + document.getElementById('url').value
    window.location.href = postURL
}

$('.toast').toast('show')
