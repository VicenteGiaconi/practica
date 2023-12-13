function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

document.getElementById('confirm').onclick = function(e) {
    const chat_name = document.getElementById('chatnameinput').value;
    const csrftoken = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/api/new-chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'chat_name': chat_name,
            'X-CSRFToken': csrftoken,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        window.location.href = 'http://127.0.0.1:8000/api/index/';
    })
    .catch((error) => console.error('error', error))
}

document.getElementById('cancel').onclick = function(e) {
    window.location.href = 'http://127.0.0.1:8000/api/index/';
}