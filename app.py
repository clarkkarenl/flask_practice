from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth

from contact_api import api
import json

app = Flask(__name__, static_url_path = "")

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'python'
    return None

@auth.error_handler
def unauthorized(error=None):
    message = {
        'status': 403,
        'message': 'Forbidden: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp
    # return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'Bad request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp
    # return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
    # return make_response(jsonify( { 'error': 'Not found' } ), 404)

# seed the store with two default records - one live and one deleted
store = {
    'foo@bar.com':
    {
        'email_address': 'foo@bar.com',
        'address_line1': '1235 Smith St.',
        'address_line2': 'Apt 999',
        'city': 'Hoserville',
        'state': 'CA',
        'zip_code': '91234',
        'phone_number': '818-555-1234',
        'is_deleted': False
    },
    'buxx@bar.com':
    {
        'email_address': 'buxx@bar.com',
        'address_line1': '1235 Pine Tree Way',
        'address_line2': '',
        'city': 'Johnson',
        'state': 'OR',
        'zip_code': '97011',
        'phone_number': '503-555-1234',
        'is_deleted': True
    },
}

# get all
# filter all by a single email address using '?email=' token
@app.route("/contact", methods=['GET'])
def get_all_or_filtered_contact():
    # if we have a key for filtering, operate on it
    email = request.args.get('email', None)
    # get all contacts
    result = api.filter(store, email)
    return jsonify(result), 200

# create one
@app.route("/contact/create", methods=['POST'])
@auth.login_required
def create_contact():
    contact = request.get_json()
    # add the request data to the store
    api.create(store, contact)
    return "OK", 201

# get specific contact
@app.route("/contact/<email>", methods=['GET'])
def get_single_contact(email):
    # get a single contact
    result = api.filter(store, email)
    if result:
        return jsonify(result), 200
    else:
        return not_found()


# delete specific contact by marking its is_deleted flag True
# alter existing contact by replacing info and returning new record
@app.route("/contact/<email>", methods=['DELETE', 'PUT'])
@auth.login_required
def delete_or_replace_single_contact(email):
    if request.method == 'DELETE':
        api.delete(store, email)
        return "OK", 201
    if request.method == 'PUT':
        result = api.replace(store, email)
        return "OK", 201

if __name__ == "__main__":
    app.run()
