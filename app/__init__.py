from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Initialize extensions first
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints/routes AFTER db is initialized
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Register KPI routes AFTER db init as well
    from .kpi import register_kpi_routes
    register_kpi_routes(app)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
