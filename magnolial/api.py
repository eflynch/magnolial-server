from flask import request, jsonify
import json
from magnolial import app, db
from magnolial.models import Magnolial, MagnolialUser

def validate_trunk(trunk):
    if 'childs' not in trunk:
        raise APIException(400, "Missing childs")
    if 'collapsed' not in trunk:
        raise APIException(400, "Missing collapsed")
    if 'completed' not in trunk:
        raise APIException(400, "Missing completed")
    if 'value' not in trunk:
        raise APIException(400, "Missing value")
    if not isinstance(trunk['childs'],list):
        raise APIException(400, "Childs is not a list")
    if not isinstance(trunk['collapsed'],bool):
        raise APIException(400, "Collapsed is not a bool")
    if not isinstance(trunk['completed'],bool):
        raise APIException(400, "Completed is not a bool")
    for c in trunk['childs']:
        validate_trunk(c)

class APIException(Exception):
    def __init__(self, status, message=None):
        self._status = status
        self._message = message
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value
    @property
    def message(self):
        if self._message:
            return self._message
        if self._status == 404:
            return 'Not found'
        if self._status == 403:
            return 'Forbidden'
        if self._status == 401:
            return 'Unauthorized'
        if self._status == 400:
            return 'Bad request'
    @message.setter
    def message(self, value):
        self._message = value

@app.errorhandler(APIException)
def handle_api_exception(error):
    resp = jsonify({'message': error.message, 'status': error.status})
    resp.status_code = error.status
    return resp

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.before_request
def verify_api():
    if request.method in ['GET', 'POST', 'PATCH']:
        if 'application/json' not in request.content_type:
            raise APIException(400, 'Requires JSON')


@app.route('/m/<filename>.mgl', methods=['GET', 'OPTIONS'])
def get_magnolial(filename):
    # Authenticate

    # Return
    magnolial = db.session.query(Magnolial).filter(Magnolial.filename == filename).first()
    if not magnolial:
        raise APIException(404, message="File not found")
       
    return jsonify(json.loads(magnolial.toJSON())) 

@app.route('/m/<filename>.mgl', methods=['POST'])
def new_magnolial(filename):
    pass
    # Authenticate

    # Verify Name is free
    if db.session.query(Magnolial).filter(Magnolial.filename == filename).first():
        raise APIException(400, message="File already exists")

    # Validate
    magnolial_json = request.get_json()
    validate_trunk(magnolial_json['trunk'])

    magnolial = Magnolial(None, filename, json.dumps(magnolial_json))
    db.session.add(magnolial)
    db.session.commit()

    return jsonify(json.loads(magnolial.toJSON()))

@app.route('/m/<filename>.mgl', methods=['PATCH'])
def update_magnolial(filename):
    # Authenticate

    magnolial = db.session.query(Magnolial).filter(Magnolial.filename == filename).first()
    if not magnolial:
        raise APIException(404, message="File not found")
    
    # Validate
    magnolial_json = request.get_json()
    validate_trunk(magnolial_json['trunk'])

    # Update
    magnolial.content = json.dumps(magnolial_json)
    db.session.commit()

    return jsonify(json.loads(magnolial.toJSON()))

