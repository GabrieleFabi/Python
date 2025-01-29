import datetime
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>Landing page for Api test</h1>"

@app.route('/date', methods=['GET'])
def get_date():
    currentDate = datetime.date.today()
    strCurrentDate = str(currentDate)
    return jsonify({'date': strCurrentDate.strip()})

@app.route('/contatti', methods=['GET'])
def get_contatti():
    tel = 123456789
    email = "gabrielefabi7@gmail.com"
    return jsonify({'telefono': tel, 'email': email})

@app.route('/time', methods=['GET'])
def get_time():
    currentTime = datetime.datetime.now().time()
    strCurrentTime = str(currentTime)
    return jsonify({'time': strCurrentTime.strip()})

if __name__ == '__main__':
    app.run()