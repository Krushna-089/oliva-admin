from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from extensions import db
from models.item import Item
from utils.decorators import admin_required
from utils.helpers import slugify

admin_items_bp = Blueprint("admin_items", __name__, url_prefix="/api/v1/admin")

@admin_items_bp.post("/items")
@admin_required
def create_item():
    d = request.get_json(silent=True) or {}
    uid = int(get_jwt_identity())
    if not d.get("sku_code") or not d.get("product_name"):
        return jsonify(success=False, message="sku_code and product_name required"), 400
    if Item.query.filter_by(sku_code=d["sku_code"]).first():
        return jsonify(success=False, message="SKU already exists"), 409

    item = Item(
        sku_code=d["sku_code"].strip().upper(),
        product_name=d["product_name"].strip(),
        category_id=d["category_id"],
        subcategory_id=d["subcategory_id"],
        viscosity_grade=d.get("viscosity_grade"),
        oil_type=d.get("oil_type", "NA"),
        compliance_rating=d.get("compliance_rating"),
        volume_litres=d["volume_litres"],
        packaging_type=d.get("packaging_type", "Bottle"),
        uom=d.get("uom", "Litre"),
        base_price=d.get("base_price", 0),
        mrp=d.get("mrp"),
        dealer_price=d.get("dealer_price"),
        stock_quantity=d.get("stock_quantity", 0),
        low_stock_alert=d.get("low_stock_alert", 10),
        short_description=d.get("short_description"),
        description=d.get("description"),
        image_url=d.get("image_url"),
        is_featured=d.get("is_featured", False),
        is_active=d.get("is_active", True),
        created_by=uid, updated_by=uid,
    )
    db.session.add(item); db.session.commit()
    return jsonify(success=True, data=item.to_dict()), 201

@admin_items_bp.put("/items/<int:iid>")
@admin_required
def update_item(iid):
    item = Item.query.get_or_404(iid)
    d = request.get_json(silent=True) or {}
    uid = int(get_jwt_identity())
    for f in ("product_name","category_id","subcategory_id","viscosity_grade",
              "oil_type","compliance_rating","volume_litres","packaging_type",
              "uom","base_price","mrp","dealer_price","stock_quantity",
              "low_stock_alert","short_description","description","image_url",
              "is_featured","is_active"):
        if f in d: setattr(item, f, d[f])
    item.updated_by = uid
    db.session.commit()
    return jsonify(success=True, data=item.to_dict())


@admin_items_bp.delete("/items/<int:iid>/hard")     # <-- NEW
@admin_required                                      # <-- NEW
def hard_delete_item(iid):                           # <-- NEW
    item = Item.query.get_or_404(iid)                # <-- NEW
    db.session.delete(item)                          # <-- NEW
    db.session.commit()                              # <-- NEW
    return jsonify(success=True,                     # <-- NEW
                   message=f"Item {iid} permanently deleted")

                   
@admin_items_bp.delete("/items/<int:iid>")
@admin_required
def delete_item(iid):
    item = Item.query.get_or_404(iid)
    item.is_active = False           # soft delete
    item.updated_by = int(get_jwt_identity())
    db.session.commit()
    return jsonify(success=True, message="Item deactivated")
    