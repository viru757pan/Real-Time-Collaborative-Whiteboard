from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store whiteboard state
whiteboard_data = []


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('draw')
def handle_draw(data):
    # Broadcast drawing data to all clients
    whiteboard_data.append(data)  # Save for persistence
    emit('draw', data, broadcast=True, include_self=False)


@socketio.on('clear')
def handle_clear():
    global whiteboard_data
    whiteboard_data = []  # Clear the whiteboard
    emit('clear', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
