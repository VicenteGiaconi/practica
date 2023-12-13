const chatLog = document.querySelector('#chat-log')

const roomId = JSON.parse(document.getElementById('room-id').textContent);

if (!chatLog.hasChildNodes()) {
    const emptyText = document.createElement('div')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'No messages'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/api/'
    + roomId
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div')
    const userToken = data['user_token']
    const loggedInUserToken = localStorage['access_token'];
    messageElement.innerText = data.message

    if (userToken===loggedInUserToken) {
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.appendChild(messageElement)
    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'room_id': roomId,
        'message': message,
        'user_token': localStorage.getItem('access_token'),
    }));
    messageInputDom.value = '';
};