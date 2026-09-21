from extensions import db
from .base import TimestampMixin

class ContactQuery(TimestampMixin, db.Model):
    __tablename__ = "contact_queries"

    id         = db.Column(db.BigInteger, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(180), nullable=False)
    phone      = db.Column(db.String(20),  nullable=False)
    subject    = db.Column(db.String(200))
    message    = db.Column(db.Text, nullable=False)
    status     = db.Column(db.Enum("new","in_progress","resolved","spam","closed"),
                           nullable=False, default="new")
    priority   = db.Column(db.Enum("low","normal","high"), nullable=False, default="normal")
    source     = db.Column(db.String(50), nullable=False, default="website")
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    admin_note = db.Column(db.Text)
    updated_by = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="SET NULL"))

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "phone": self.phone, "subject": self.subject, "message": self.message,
            "status": self.status, "priority": self.priority,
            "source": self.source, "admin_note": self.admin_note,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }
        