from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from extensions import db, limiter
from models.contact import ContactQuery
from utils.decorators import admin_required

contact_bp = Blueprint("contact", __name__, url_prefix="/api/v1")

# ---------- PUBLIC (called from website contact form) ----------
@contact_bp.post("/contact")
@limiter.limit("20 per minute")
def create_contact():
    data = request.get_json(silent=True) or {}
    required = ("name", "email", "phone", "message")
    if not all((data.get(f) or "").strip() for f in required):
        return jsonify(success=False, message="name, email, phone, message are required"), 400

    # simple honeypot — website adds hidden field "website_url"
    if (data.get("website_url") or "").strip():
        return jsonify(success=True, message="Thank you"), 201

    cq = ContactQuery(
        name=data["name"].strip()[:120],
        email=data["email"].strip().lower()[:180],
        phone=data["phone"].strip()[:20],
        subject=(data.get("subject") or "")[:200] or None,
        message=data["message"].strip(),
        source=(data.get("source") or "website")[:50],
        ip_address=request.remote_addr,
        user_agent=(request.headers.get("User-Agent") or "")[:255],
    )
    db.session.add(cq)
    db.session.commit()
    return jsonify(success=True, message="Thank you, we'll get back to you soon.",
                   data={"id": cq.id}), 201

# ---------- ADMIN ----------
@contact_bp.get("/admin/contact-queries")
@admin_required
def list_contacts():
    page     = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    status   = request.args.get("status")
    search   = request.args.get("q")

    q = ContactQuery.query
    if status: q = q.filter(ContactQuery.status == status)
    if search:
        like = f"%{search}%"
        q = q.filter(db.or_(ContactQuery.name.ilike(like),
                            ContactQuery.email.ilike(like),
                            ContactQuery.phone.ilike(like),
                            ContactQuery.subject.ilike(like)))
    p = q.order_by(ContactQuery.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return jsonify(success=True, data={
        "items": [c.to_dict() for c in p.items],
        "pagination": {"page": p.page, "per_page": p.per_page,
                       "total": p.total, "pages": p.pages},
    })

@contact_bp.get("/admin/contact-queries/<int:qid>")
@admin_required
def get_contact(qid):
    cq = ContactQuery.query.get_or_404(qid)
    return jsonify(success=True, data=cq.to_dict())

@contact_bp.patch("/admin/contact-queries/<int:qid>")
@admin_required
def update_contact(qid):
    cq = ContactQuery.query.get_or_404(qid)
    data = request.get_json(silent=True) or {}
    uid = int(get_jwt_identity())

    if "status" in data:
        if data["status"] not in ("new","in_progress","resolved","spam","closed"):
            return jsonify(success=False, message="Invalid status"), 400
        cq.status = data["status"]
    if "priority" in data: cq.priority = data["priority"]
    if "admin_note" in data: cq.admin_note = data["admin_note"]

    cq.updated_by = uid
    db.session.commit()
    return jsonify(success=True, data=cq.to_dict())
