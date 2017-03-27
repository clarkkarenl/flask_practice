from flask import Flask, jsonify, request

import api
import json


app = Flask(__name__)
# seed the store with a default record
store = {
    'foo@bar.com':
    {
        'email_address': 'foo@bar.com',
        'address_line1': '1235 Smith St.',
        'address_line2': 'Apt 999',
        'city': 'Hoserville',
        'state': 'CA',
        'zip_code': '91234',
        'phone_number': '1-818-555-1234',
        'is_deleted': False
    },
    'buxx@bar.com':
    {
        'email_address': 'buxx@bar.com',
        'address_line1': '1235 Pine Tree Way',
        'address_line2': '',
        'city': 'Johnson',
        'state': 'OR',
        'zip_code': '97008',
        'phone_number': '1-503-555-1234',
        'is_deleted': True
    },
}

# TODO LIST:
# login:
## - did I get auth?
## - un-base64 it
## - does ^ version of auth match expected?
## if yes, proceed, if no, 401
# validation:
## contemplate validation of some sort
# tests!

# get all
# create one
# search for email addy
@app.route("/contact", methods=['GET', 'POST'])
# TODO rename this damn thing
def do_stuff():
    if request.method == 'GET':
        # if we have a key for filtering, operate on it
        email = request.args.get('email', None)
        # get all contacts
        result = api.filter(store, email)
        return jsonify(result)
    if request.method == 'POST':
        # create contact
        contact = request.get_json()
        api.create(store, contact)
        return "OK", 201

# get specific contact
# delete a contact by marking its is_deleted flag True
@app.route("/contact/<email>", methods=['GET', 'DELETE'])
def get_contact(email):
    # get a single contact
    if request.method == 'GET':
        result = api.get(store, email)
        return jsonify(result)
    if request.method == 'DELETE':
        api.delete(store, email)
        return "OK", 200


if __name__ == "__main__":
    app.run()
