from flask import Blueprint, render_template
from flask import request

home = Blueprint(__name__, "home")


@home.route("/")
def homeRoute():
    code = request.args.get('code')
    return render_template("home.html", code=code)
