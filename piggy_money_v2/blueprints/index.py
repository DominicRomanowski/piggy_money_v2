
from flask import Blueprint, request, session, redirect, url_for, \
     render_template, render_template_string, jsonify

from piggy_money_v2.db.dbaccess import get_user_pass, get_user_accounts

import os

bp = Blueprint('piggy_money', __name__)

@bp.after_request
def add_header(r):
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-control"] = "public, max-age=0"
    return r


@bp.route("/")
def index():
    with open("./piggy_money_v2/templates/index.html") as f:
        template = f.read()
    return render_template_string(template)
    #return render_template('index.html')

@bp.route("/api/test")
def api_test():
    return jsonify({'content':"%c🤡", 'style':'background-color:yellow;border:5px solid black;font-size:3rem;color:white;border-radius:1000px;padding:10px'})

@bp.route("/api/get_user_accounts/", methods=["POST"])
def api_get_user_accounts():
    data = request.get_json()
    # TODO: user tokens
    if "username" not in data:
        return jsonify({"valid":False})
    username = data["username"]

    # TODO: check user has accounts
    db_accounts = get_user_accounts(username)

    return jsonify({"valid":True,"accounts":db_accounts})


@bp.route("/api/authenticate/", methods=["POST"])
def api_authenticate():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify({"valid":False})

    username = data["username"]
    password = data["password"]
    db_pass = get_user_pass(username)
    if len(db_pass) > 1:
        #TODO: log error, reject, should only be one result
        pass

    if len(db_pass) == 1:
        if db_pass[0][0] == password:
            return jsonify({"valid":True,"token":"abcdef1234567890"})

    return jsonify({"valid":False})
