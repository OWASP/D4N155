from flask import Flask
from flask import jsonify
import os
os.sys.path.append('getrails/')
from getrails.search import search_now
os.sys.path.append('modules/')
from generator import main

port = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
msg = "Its OWASP D4N155 project for API, see: https://github.com/OWASP/D4N155, branch: api"
    
# See all data
@app.route('/')
def index():
    # Get all registers in DB
    response.headers['Access-Control-Allow-Origin'] = '*'
    return jsonify(result = "Get all data", helpus = "{}".format(msg))

# See all urls of domain
@app.route('/domain/<param>')
def domain(param):
    # Get id in DB
    get_urls = search_now("site:{}".format(param))
    response = jsonify(result = get_urls, helpus = "{}".format(msg))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Make new analyze
@app.route('/make/<param>')
def make(param):
    response = jsonify(result = main(param), helpus = "{}".format(msg))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=port)
