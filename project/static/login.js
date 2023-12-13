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


document.getElementById('submit').onclick = function(e) {
    const username = document.getElementById('usernameinput').value;
    const password = document.getElementById('passwordinput').value;
    const csrftoken = getCookie('csrftoken');
    fetch('http://127.0.0.1:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'username': username,
            'password': password,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data['error']) {
            const errorDiv = document.querySelector('#error-message')
            const p = document.createElement('p')
            p.innerText = 'Usuario no existe';
            errorDiv.appendChild(p)
        } else {
            fetch('http://127.0.0.1:8000/tokens/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'username': username,
                    'password':password,
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.access);
                window.location.href = 'http://127.0.0.1:8000/api/index/';
            })
            .catch((error) => console.error('error', error));
        }
    })
    .catch((error) => console.error('error', error));
}