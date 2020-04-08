import json
import logging
import os
import time

from flask import Flask, request, jsonify, Response, g

from dicttoxml import dicttoxml
from marshmallow import ValidationError

from src.estimator import estimator
from src.log import __file_handler
from src.serializer import DataSerializer


app = Flask(__name__)
app.logger.addHandler(__file_handler)
app.logger.setLevel(logging.INFO)


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    if request.endpoint in ['estimator', 'estimator_xml']:
        app.logger.info(response.status_code)
    return response


@app.route('/api/v1/on-covid-19', methods=['POST'], endpoint='estimator')
@app.route('/api/v1/on-covid-19/json', methods=['POST'], endpoint="estimator")
def estimate_effects():
    """Estimates the effect of COVID-19 based on the data passed."""
    if not request.json:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": {"general": "Json data required"}}), 400

    serializer = DataSerializer()
    try:
        data = serializer.load(request.get_json())
    except ValidationError as err:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": err.messages}), 400

    return Response(response=json.dumps(estimator(data)), status=200, content_type='application/json')


@app.route('/api/v1/on-covid-19/xml', methods=['POST'], endpoint='estimator_xml')
def estimate_effects_xml():
    """Estimates the effects of COVID-19 and returns data in XML format."""
    if not request.json:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {},
                        "errors": {"general": "Json data required"}}), 400

    serializer = DataSerializer()
    try:
        data = serializer.load(request.get_json())
    except ValidationError as err:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": err.messages}), 400

    xml = dicttoxml(data)
    return Response(response=xml, status=200, mimetype='text/xml')


@app.route('/api/v1/on-covid-19/logs', methods=['GET'], endpoint='logs')
def extract_logs():
    file = os.path.join(os.path.dirname(__file__), 'src/access.log')
    data = ""
    with open(file, 'r') as f:
        data = f.read()

    return Response(response=data, status=200, mimetype='text/plain')


if __name__ == "__main__":
    app.run(debug=True)
