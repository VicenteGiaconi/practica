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
    const password1 = document.getElementById('passwordinput1').value;
    const password2 = document.getElementById('passwordinput2').value;
    const email = document.getElementById('emailinput').value;
    const csrftoken = getCookie('csrftoken');
    if (password1 === password2) {
        fetch('http://127.0.0.1:8000/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'username': username,
                'password': password1,
                'email': email,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            window.location.href = 'http://127.0.0.1:8000/login/';
        })
        .catch((error) => console.error('error', error));
    } else {
        console.log('la contraseña no coincide')
    }
}