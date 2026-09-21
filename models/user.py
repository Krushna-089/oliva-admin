import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from .base import TimestampMixin

class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id              = db.Column(db.BigInteger, primary_key=True)
    uuid            = db.Column(db.String(36), unique=True, nullable=False,
                                default=lambda: str(uuid.uuid4()))
    full_name       = db.Column(db.String(120), nullable=False)
    email           = db.Column(db.String(180), unique=True, nullable=False, index=True)
    phone           = db.Column(db.String(20))
    password_hash   = db.Column(db.String(255), nullable=False)
    user_type       = db.Column(db.Enum("admin","employee","distributor","retailer"),
                                nullable=False, default="admin")
    role_code       = db.Column(db.String(50), nullable=False, default="SUPER_ADMIN")
    profile_image   = db.Column(db.String(255))
    is_active       = db.Column(db.Boolean, nullable=False, default=True)
    is_locked       = db.Column(db.Boolean, nullable=False, default=False)
    failed_attempts = db.Column(db.SmallInteger, nullable=False, default=0)
    last_login_at   = db.Column(db.DateTime)
    last_login_ip   = db.Column(db.String(45))
    created_by      = db.Column(db.BigInteger)
    updated_by      = db.Column(db.BigInteger)
    deleted_at      = db.Column(db.DateTime)

    def set_password(self, raw): self.password_hash = generate_password_hash(raw)
    def check_password(self, raw): return check_password_hash(self.password_hash, raw)

    def to_dict(self):
        return {
            "id": self.id, "uuid": self.uuid, "full_name": self.full_name,
            "email": self.email, "phone": self.phone,
            "user_type": self.user_type, "role_code": self.role_code,
            "is_active": self.is_active,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat(),
        }
        