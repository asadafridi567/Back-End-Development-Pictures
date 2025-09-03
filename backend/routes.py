from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200
    return jsonify({"message": f"Picture with id {id} not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if not new_picture:
        abort(400, "Invalid JSON data")

    # Assuming a new ID is generated
    new_id = max(p['id'] for p in data) + 1 if data else 1
    new_picture['id'] = new_id
    data.append(new_picture)

    response = jsonify(new_picture)
    response.status_code = 201
    response.headers['Location'] = url_for('get_picture_by_id', id=new_id)
    return response


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_data = request.get_json()
    if not update_data:
        abort(400, "Invalid JSON data")

    for picture in data:
        if picture['id'] == id:
            picture.update(update_data)
            return jsonify(picture), 200

    return jsonify({"message": f"Picture with id {id} not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    original_len = len(data)
    data = [picture for picture in data if picture['id'] != id]
    if len(data) < original_len:
        return '', 204

    return jsonify({"message": f"Picture with id {id} not found"}), 404
