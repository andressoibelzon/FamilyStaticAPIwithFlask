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
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    if members is None:
        return jsonify({"msg":"no members"}), 400
    return jsonify({"msg":"ok"}, {"family": members}), 200



    # obtiene los datos de un SOLO member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    ## querys o consultas
    if member is None:
        return jsonify({"msg":"no id match"}), 400
    return jsonify({"msg": "ok"}, {"result": member}), 200

    # anade un miembro a la familia
@app.route('/member', methods=['POST'])
def create_member():
    json_data = request.get_json()
    member = jackson_family.add_member(json_data)
    ## querys o consultas

    if member is None:
        return jsonify({"msg":"error"}), 400
    return jsonify({"msg": "ok"}, {"result": member}), 200


    # elimina un miembro de la familia
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    member = jackson_family.delete_member(member_id)

    if member is None:
        return jsonify({"msg":"error"}), 400
    return jsonify({"msg": "ok"},{"result": member}), 200








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
