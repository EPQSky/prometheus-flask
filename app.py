import json

from flask import Flask, request

import Alert

app = Flask(__name__)


@app.route('/alert-info', methods=['POST'])
def alert_data():
    data = request.get_data()
    json_re = json.loads(data)
    json.dumps(json_re)
    print(json_re)
    Alert.send_alert(json_re)
    return json_re


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
