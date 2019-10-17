from flask import Flask
from flask import jsonify
import os
os.sys.path.append('modules/')
from generator import main

app = Flask(__name__)
    
# See all report
@app.route('/')
def index():
    # Get all registers in DB
    return jsonify(result = "Get all registers")

@app.route('/<param>')
def show(param):
    # Get id in DB
    return jsonify(result = "Get register based in id: {}".format(param))
    del param

# Make new analyze
@app.route('/gen/<param>')
def gen(param):
    # Registerj in DB
    resp = jsonify(result = main(param))
    return resp

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
