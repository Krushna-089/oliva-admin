# category.py
from extensions import db
from .base import TimestampMixin

class Category(TimestampMixin, db.Model):
    __tablename__ = "categories"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    slug        = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url   = db.Column(db.String(255))
    sort_order  = db.Column(db.Integer, default=0, nullable=False)
    is_active   = db.Column(db.Boolean, default=True, nullable=False)
    created_by  = db.Column(db.BigInteger)
    updated_by  = db.Column(db.BigInteger)

    subcategories = db.relationship("SubCategory", back_populates="category",
                                    cascade="all, delete-orphan",
                                    order_by="SubCategory.sort_order")

    def to_dict(self, with_subs=False):
        d = {"id": self.id, "name": self.name, "slug": self.slug,
             "description": self.description, "image_url": self.image_url,
             "sort_order": self.sort_order, "is_active": self.is_active}
        if with_subs:
            d["subcategories"] = [s.to_dict() for s in self.subcategories if s.is_active]
        return d