window.addEventListener('load', function() {
    fetch('/clear_session', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => console.error('Error:', error));
});
