from flask import Flask
from flask import jsonify
import os
os.sys.path.append('modules/')
import generator

app = Flask(__name__)

@app.route('/<param>')
def hello_world(param):
    results = os.popen("python3 modules/generator.py "+param).read()
    resp = jsonify(result = results)
    return resp

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
