from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from extensions import db, limiter
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.post("/login")
@limiter.limit("10 per minute")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify(success=False, message="Email and password are required"), 400

    user = User.query.filter_by(email=email, deleted_at=None).first()
    if not user or not user.check_password(password):
        return jsonify(success=False, message="Invalid credentials"), 401
    if not user.is_active or user.is_locked:
        return jsonify(success=False, message="Account disabled"), 403

    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    db.session.commit()

    claims = {"user_type": user.user_type, "role_code": user.role_code}
    return jsonify(success=True, data={
        "access_token":  create_access_token(identity=str(user.id), additional_claims=claims),
        "refresh_token": create_refresh_token(identity=str(user.id)),
        "user": user.to_dict(),
    })

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    user = User.query.get(int(uid))
    claims = {"user_type": user.user_type, "role_code": user.role_code}
    return jsonify(success=True, data={
        "access_token": create_access_token(identity=str(user.id), additional_claims=claims)
    })

@auth_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(int(uid))
    return jsonify(success=True, data=user.to_dict())
    