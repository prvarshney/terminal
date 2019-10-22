from database import DBQuery as db
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/",methods=['POST'])
def authentication():
    user_credentials = request.get_json()
    print(user_credentials['user_id'])
    print(user_credentials['password'])
    response = { 'status':'300' }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,port=5001,host="0.0.0.0")