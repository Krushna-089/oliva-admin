from flask import Flask, jsonify
from config import Config
from extensions import db, migrate, jwt, cors, limiter

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    limiter.init_app(app)

    from routes.auth import auth_bp
    from routes.contact import contact_bp
    from routes.catalog import catalog_bp
    from routes.admin_items import admin_items_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(admin_items_bp)

    @app.get("/health")
    def health(): return {"status": "ok"}

    @app.errorhandler(404)
    def nf(e): return jsonify(success=False, message="Not found"), 404

    @app.errorhandler(500)
    def se(e):
        db.session.rollback()
        return jsonify(success=False, message="Server error"), 500

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
    