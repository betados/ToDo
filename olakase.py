from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
 



 
@app.route("/")

def hello():
    return "Ola k ase!"
 
@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)
 
if __name__ == '__main__':
    app.run(port=8080, debug=True)