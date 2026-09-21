# subcategory.py
from extensions import db
from .base import TimestampMixin

class SubCategory(TimestampMixin, db.Model):
    __tablename__ = "subcategories"
    id          = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id",
                            ondelete="CASCADE"), nullable=False)
    name        = db.Column(db.String(120), nullable=False)
    slug        = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url   = db.Column(db.String(255))
    sort_order  = db.Column(db.Integer, default=0, nullable=False)
    is_active   = db.Column(db.Boolean, default=True, nullable=False)
    created_by  = db.Column(db.BigInteger)
    updated_by  = db.Column(db.BigInteger)

    category = db.relationship("Category", back_populates="subcategories")

    def to_dict(self):
        return {"id": self.id, "category_id": self.category_id, "name": self.name,
                "slug": self.slug, "description": self.description,
                "image_url": self.image_url, "is_active": self.is_active}