from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = """
<!DOCTYPE html>
<html>
<head><title>Live Lobby</title></head>
<body>
    <h1>Live Lobby</h1>
    <div id="messages"></div>
    <br>
    <input id="name" placeholder="Your name" />
    <button onclick="send()">Send / Join</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
    <script>
        const socket = io();
        socket.on('message', msg => {
            document.getElementById('messages').innerHTML += <p>${msg}</p>;
        });
        function send() {
            const name = document.getElementById('name').value || 'Anonymous';
            socket.emit('message', name + ' joined the lobby');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('message')
def handle_message(data):
    print('Received:', data)
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)