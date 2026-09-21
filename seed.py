from app import create_app
from extensions import db
from models.user import User
from models.category import Category
from models.subcategory import SubCategory
from utils.helpers import slugify

CATALOG = {
    "Two-Wheelers (Moto Gear)": [
        "4T Engine Oil", "Scooter/Gearless Oil",
        "Front Fork Oil", "Chain Lubricants",
    ],
    "Four-Wheelers & Passenger Cars": [
        "Petrol Engine Oil", "Diesel Engine Oil", "CNG-Specific Oil",
    ],
    "Commercial & Heavy Duty": [
        "Tractor Oil", "Heavy-Duty Diesel Engine Oil (HDDEO)", "Hydraulic Oil",
    ],
    "Industrial & Traded Lines": [
        "Recycled Base Oil", "Third-Party Lubricants",
    ],
}

def run():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@olivamotogear.com").first():
            u = User(full_name="Super Admin",
                     email="admin@olivamotogear.com",
                     phone="0000000000",
                     user_type="admin", role_code="SUPER_ADMIN")
            u.set_password("ChangeMe@123")
            db.session.add(u)
            print("✔ Admin created → admin@olivamotogear.com / ChangeMe@123")

        for i, (cname, subs) in enumerate(CATALOG.items(), start=1):
            cat = Category.query.filter_by(slug=slugify(cname)).first()
            if not cat:
                cat = Category(name=cname, slug=slugify(cname), sort_order=i)
                db.session.add(cat); db.session.flush()
                print(f"✔ Category: {cname}")

            for j, sname in enumerate(subs, start=1):
                sslug = slugify(f"{cname}-{sname}")
                if not SubCategory.query.filter_by(slug=sslug).first():
                    db.session.add(SubCategory(category_id=cat.id, name=sname,
                                               slug=sslug, sort_order=j))
        db.session.commit()
        print("✔ Seed complete")

if __name__ == "__main__":
    run()
    