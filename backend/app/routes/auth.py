from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta

from ..extensions import db
from ..models import User
from ..security import hash_password, verify_password, email_fingerprint, encrypt_email, decrypt_email

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def _jwt_durations(cfg):
    return (
        timedelta(minutes=int(cfg.get("JWT_ACCESS_TOKEN_EXPIRES_MIN", 15))),
        timedelta(days=int(cfg.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))),
    )


@bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: user@example.com
              password:
                type: string
                example: secret123
              full_name:
                type: string
                example: John Doe
            required:
              - email
              - password
    responses:
      201:
        description: User successfully registered
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                access_token:
                  type: string
                refresh_token:
                  type: string
                user:
                  type: object
      400:
        description: Missing email or password
      409:
        description: User already exists
    """
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    email_hash = email_fingerprint(email)
    existing = User.query.filter_by(email_hash=email_hash).first()
    if existing:
        return jsonify({"error": "user already exists"}), 409

    key = current_app.config.get("EMAIL_ENC_KEY")
    if not key:
        return jsonify({"error": "server misconfigured: EMAIL_ENC_KEY missing"}), 500

    email_enc = encrypt_email(email, key)
    pwd_hash = hash_password(password)

    user = User(email_enc=email_enc, email_hash=email_hash, password_hash=pwd_hash, full_name=full_name)
    db.session.add(user)
    db.session.commit()

    access_exp, refresh_exp = _jwt_durations(current_app.config)
    access = create_access_token(identity=str(user.id), expires_delta=access_exp)
    refresh = create_refresh_token(identity=str(user.id), expires_delta=refresh_exp)

    return jsonify({
        "message": "registered",
        "access_token": access,
        "refresh_token": refresh,
        "user": user.to_public(email_plain=email),
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    """
    User login
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: user@example.com
              password:
                type: string
                example: secret123
            required:
              - email
              - password
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                access_token:
                  type: string
                refresh_token:
                  type: string
                user:
                  type: object
      401:
        description: Invalid credentials
    """
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    email_hash = email_fingerprint(email)
    user = User.query.filter_by(email_hash=email_hash).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "invalid credentials"}), 401

    access_exp, refresh_exp = _jwt_durations(current_app.config)
    access = create_access_token(identity=str(user.id), expires_delta=access_exp)
    refresh = create_refresh_token(identity=str(user.id), expires_delta=refresh_exp)

    key = current_app.config.get("EMAIL_ENC_KEY")
    email_plain = decrypt_email(user.email_enc, key) if key else None

    return jsonify({
        "message": "logged_in",
        "access_token": access,
        "refresh_token": refresh,
        "user": user.to_public(email_plain=email_plain),
    }), 200


@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
    Get current user info
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Returns user information
        content:
          application/json:
            schema:
              type: object
              properties:
                id: {type: integer}
                email: {type: string}
                full_name: {type: string}
                created_at: {type: string}
                updated_at: {type: string}
      401:
        description: Unauthorized (missing or invalid token)
      404:
        description: User not found
    """
    uid = get_jwt_identity()
    user = User.query.get(int(uid))

    if not user:
        return jsonify({"error": "not found"}), 404

    key = current_app.config.get("EMAIL_ENC_KEY")
    email_plain = decrypt_email(user.email_enc, key) if key else None
    return jsonify(user.to_public(email_plain=email_plain)), 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: New access token
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
      401:
        description: Invalid or expired refresh token
    """
    uid = get_jwt_identity()
    access_exp, _ = _jwt_durations(current_app.config)
    new_access = create_access_token(identity=str(uid), expires_delta=access_exp)
    return jsonify({"access_token": new_access}), 200
