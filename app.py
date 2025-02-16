from flask import Flask, render_template, request, redirect, url_for, flash
from app import db

def create_app():
    app = Flask(__name__)

    # Configure the app (replace with your actual database details)
    app.secret_key = "abcd@1234"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Panda#2001@localhost:3306/fitness_center"  # Ensure this is correct
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from services.user_management.user import user_bp  # Ensure this module exists and is correctly implemented
    app.register_blueprint(user_bp)
    from services.admin.memberships import memberships_bp
    app.register_blueprint(memberships_bp)

    return app

if __name__ == "__main__":
    app = create_app()

    @app.route('/')
    def home():
        return render_template('init_home.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/send_message', methods=['POST'])
    def send_message():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle sending message (e.g., save to database, send email, etc.)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    # Ensure database tables are created before running the app
    with app.app_context():
        db.create_all()

    # Run the application
    app.run(debug=True)
