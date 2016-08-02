import json
from flask import Flask, Response
from balance import Balance

balance = Balance()
app = Flask(__name__,  static_url_path="", static_folder="public")

@app.route('/balances')
def balances_all():
    balances = [{
      'id': x[0],
      'timestamp': x[1],
      'weight': x[2],
      'user_id': x[3]
    } for x in balance.all()]
    response = Response(json.dumps(balances),  mimetype='application/json')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
