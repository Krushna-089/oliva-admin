# item.py
from extensions import db
from .base import TimestampMixin

class Item(TimestampMixin, db.Model):
    __tablename__ = "items"
    id                = db.Column(db.Integer, primary_key=True)
    sku_code          = db.Column(db.String(60), unique=True, nullable=False)
    product_name      = db.Column(db.String(200), nullable=False)
    category_id       = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    subcategory_id    = db.Column(db.Integer, db.ForeignKey("subcategories.id"), nullable=False)
    viscosity_grade   = db.Column(db.String(40))
    oil_type          = db.Column(db.Enum("Mineral","Semi-Synthetic","Fully Synthetic","NA"),
                                  nullable=False, default="NA")
    compliance_rating = db.Column(db.String(120))
    volume_litres     = db.Column(db.Numeric(8,2), nullable=False)
    packaging_type    = db.Column(db.Enum("Bottle","Pouch","Can","Bucket","Drum","Barrel","Other"),
                                  nullable=False, default="Bottle")
    uom               = db.Column(db.String(20), nullable=False, default="Litre")
    base_price        = db.Column(db.Numeric(10,2), nullable=False, default=0)
    mrp               = db.Column(db.Numeric(10,2))
    dealer_price      = db.Column(db.Numeric(10,2))
    stock_quantity    = db.Column(db.Integer, nullable=False, default=0)
    low_stock_alert   = db.Column(db.Integer, nullable=False, default=10)
    short_description = db.Column(db.String(300))
    description       = db.Column(db.Text)
    image_url         = db.Column(db.String(255))
    is_featured       = db.Column(db.Boolean, nullable=False, default=False)
    is_active         = db.Column(db.Boolean, nullable=False, default=True)
    created_by        = db.Column(db.BigInteger)
    updated_by        = db.Column(db.BigInteger)

    category    = db.relationship("Category")
    subcategory = db.relationship("SubCategory")

    def to_dict(self):
        return {
            "id": self.id, "sku_code": self.sku_code,
            "product_name": self.product_name,
            "category":    self.category.name    if self.category else None,
            "category_slug": self.category.slug  if self.category else None,
            "subcategory": self.subcategory.name if self.subcategory else None,
            "subcategory_slug": self.subcategory.slug if self.subcategory else None,
            "viscosity_grade": self.viscosity_grade,
            "oil_type": self.oil_type,
            "compliance_rating": self.compliance_rating,
            "volume_litres": float(self.volume_litres),
            "packaging_type": self.packaging_type,
            "uom": self.uom,
            "base_price": float(self.base_price),
            "mrp": float(self.mrp) if self.mrp else None,
            "dealer_price": float(self.dealer_price) if self.dealer_price else None,
            "stock_quantity": self.stock_quantity,
            "short_description": self.short_description,
            "description": self.description,
            "image_url": self.image_url,
            "is_featured": self.is_featured,
            "is_active": self.is_active,
        }