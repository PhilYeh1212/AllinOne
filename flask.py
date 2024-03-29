from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    # 在這裡處理伺服器收到的訊息，然後發送到所有客戶端
    socketio.emit('update', message)

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0', port=8000)