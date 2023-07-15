from flask import Flask
import env

app = Flask(__name__)

@app.route('/res1')
def index():
    return "res1"

@app.route('/res2')
def api_data():
    return "res2"

if __name__ == '__main__':
    app.run(port=env.POOL_RESTAURANTS_PORT)
