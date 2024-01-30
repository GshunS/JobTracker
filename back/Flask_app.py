from flask import Flask, jsonify
from flask_cors import CORS
import Mysql_app as sql

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def get_all():
    data = sql.queryAll()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
