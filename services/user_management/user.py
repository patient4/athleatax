from flask import Blueprint, redirect, request, jsonify, render_template, url_for
from app import db
import pdb
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import parse_qs
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="templates", static_folder="static")

@user_bp.route("/register", methods=["POST", "GET"])
def register():
    # pdb.set_trace()
    try:
        if request.method == "GET":
            return render_template("signup.html")

        # Parse JSON payload ideally we should create Parser classes TODO: create parser for generic responses.
        form_data = request.form
        email = form_data.get('email')
        password = form_data.get('password')
        if password != form_data.get('confirmation'):
            return jsonify({"error": "password should match."}), 400
        # Validate required fields
        if not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new User object
        print(email, hashed_password)
        new_user = User(email=email, password=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for(".login"))

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"errors": str(e)}), 500

    except Exception as e:
        print(e)
        return jsonify({"errorl": str(e)}), 500

@user_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("signin.html")
    try:
        form_data = request.form
        email = form_data.get('email')
        password = form_data.get('password')

        # Validate required fields
        if not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return jsonify({"success": "user logged in successfully"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

