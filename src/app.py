"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def show_all_members():
    my_members = jackson_family.get_all_members()
    return jsonify(my_members)

    

@app.route('/member/<int:member_id>', methods=['GET'])
def show_one_member(member_id):
    my_member_with_id = jackson_family.get_member(member_id)
    return jsonify(my_member_with_id)

@app.route('/members', methods=['POST'])
def create_one_member():
    new_member = jackson_family.add_member(request.json)
    return jsonify(new_member)



@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    delete_member_with_id = jackson_family.delete_member(member_id)
    return jsonify(delete_member_with_id)





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
