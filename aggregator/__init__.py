from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['upstreams'] = [f"http://api{i}:5000" for i in [1,2,3]]
    return app
