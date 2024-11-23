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

John = {
    "first_name": "John",
    #"last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]

}

Jane = {
    "first_name": "Jane",
    #"last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy ={
    "first_name": "Jimmy",
    #"last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": 1
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)





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
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#GET single member
@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

#POST
@app.route('/member', methods=['POST'])
def add_a_member():
    member = request.json
    print(f'{member} added!')
    jackson_family.add_member(member)
    if member != None:
        return "Successfully added", 200

#DELETE
@app.route('/member/<int:id>', methods=['DELETE'])
def remove_a_member():
    #retrieve the member using the get_member(id) method in FamilyStructure
    member = jackson_family.get_member(id)
    #if the member exists,
    if member:
        jackson_family.delete_member(id)
        return jsonify({
            "message": "Successfully deleted",
            "done": True
        }), 200
        #can use the delete_member(id) method
        #return a jsonified message stating that the member was successfully removed (200)
    #else
       # r#retun a jsonified message stating that the member does not exist (404)
       return jsonify({
            "message": "Member not found",
            "done": False
        }), 404
    





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
