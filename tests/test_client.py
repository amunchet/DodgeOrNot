import pytest
import threading
import multiprocessing
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/shutdown')
def shutdown():
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    shutdown_server()
    return 'Server shutting down...'

def run_server():
    app.run()

@pytest.fixture(scope='session', autouse=True)
def setup():

    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()

    proc = multiprocessing.Process(target=run_server, args=())
    proc.start()
    yield
    # Shut down the server when the thread rejoins the main thread
    requests.get('http://localhost:5000/shutdown')
    
    proc.terminate()
    #server_thread.raise_exc(SystemExit)
    # server_thread.join()

def test_server(setup, request):
    # Test the server here
    pass