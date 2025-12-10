#Created my own multipleplayer local server to test and break for QA purposes

from flask import Flask, render_template_string 
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#Plain white HTML page to enter player name to enter the server
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

@socketio.on('message') #this is to see in terminal when players has entered the server, the backend picks up the data and shows player has successfully joined
def handle_message(data):
    print('Received:', data)
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) #this is to create my own local multipleplayer server