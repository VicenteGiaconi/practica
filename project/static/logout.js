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

document.getElementById('yes').onclick = function(e) {
    const csrftoken = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'token': localStorage.getItem('access_token')
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        window.location.href = 'http://127.0.0.1:8000/login/';
    })
    .catch((error) => console.error('error', error));
};

document.getElementById('no').onclick = function(e) {
    window.location.href = 'http://127.0.0.1:8000/api/index/';
};