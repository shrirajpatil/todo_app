from app import app
from models import get_db_connection  # Import your DB connection function

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        get_db_connection.create_all()
    # Run the Flask application
    app.run(debug=True)
