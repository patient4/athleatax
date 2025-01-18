from flask import Flask
from app import db

def create_app():
    app = Flask(__name__)

    # Configure the app (replace with your actual database details)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/athleatx"  # Ensure this is correct
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from services.user_management.user import user_bp  # Ensure this module exists and is correctly implemented
    app.register_blueprint(user_bp)

    return app

if __name__ == "__main__":
    app = create_app()

    # Ensure database tables are created before running the app
    with app.app_context():
        db.create_all()

    # Run the application
    app.run(debug=True)
