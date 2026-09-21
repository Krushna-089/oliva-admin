from flask import Blueprint, request, jsonify
from extensions import db
from models.category import Category
from models.subcategory import SubCategory
from models.item import Item

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api/v1")

@catalog_bp.get("/categories")
def list_categories():
    with_subs = request.args.get("with_subcategories", "0") == "1"
    cats = (Category.query.filter_by(is_active=True)
            .order_by(Category.sort_order, Category.name).all())
    return jsonify(success=True,
                   data=[c.to_dict(with_subs=with_subs) for c in cats])

@catalog_bp.get("/categories/<slug>/subcategories")
def list_subcategories(slug):
    cat = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    subs = (SubCategory.query.filter_by(category_id=cat.id, is_active=True)
            .order_by(SubCategory.sort_order).all())
    return jsonify(success=True, data=[s.to_dict() for s in subs])

@catalog_bp.get("/items")
def list_items():
    page     = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 24)), 100)

    q = Item.query.filter_by(is_active=True)

    if cat := request.args.get("category"):
        q = q.join(Category).filter(Category.slug == cat)
    if sub := request.args.get("subcategory"):
        q = q.join(SubCategory, Item.subcategory_id == SubCategory.id)\
             .filter(SubCategory.slug == sub)
    if vis := request.args.get("viscosity"):
        q = q.filter(Item.viscosity_grade == vis)
    if ot := request.args.get("oil_type"):
        q = q.filter(Item.oil_type == ot)
    if pt := request.args.get("packaging"):
        q = q.filter(Item.packaging_type == pt)
    if search := request.args.get("q"):
        like = f"%{search}%"
        q = q.filter(db.or_(Item.product_name.ilike(like),
                            Item.sku_code.ilike(like),
                            Item.compliance_rating.ilike(like)))
    if request.args.get("featured") == "1":
        q = q.filter(Item.is_featured.is_(True))

    p = q.order_by(Item.is_featured.desc(), Item.product_name)\
         .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(success=True, data={
        "items": [i.to_dict() for i in p.items],
        "pagination": {"page": p.page, "per_page": p.per_page,
                       "total": p.total, "pages": p.pages},
    })

@catalog_bp.get("/items/<sku>")
def get_item(sku):
    item = Item.query.filter_by(sku_code=sku, is_active=True).first_or_404()
    return jsonify(success=True, data=item.to_dict())

@catalog_bp.get("/filters")
def filters():
    """Returns dropdown values for website filter panel."""
    vis = [r[0] for r in db.session.query(Item.viscosity_grade)
           .filter(Item.is_active==True, Item.viscosity_grade.isnot(None))
           .distinct().all()]
    ots = [r[0] for r in db.session.query(Item.oil_type)
           .filter(Item.is_active==True).distinct().all()]
    return jsonify(success=True, data={"viscosity_grades": vis, "oil_types": ots})
    