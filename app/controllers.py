from flask import Blueprint, redirect, url_for
from flask_security import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
    return current_user.user_name
    # return redirect(url_for("/dashboard/"))
