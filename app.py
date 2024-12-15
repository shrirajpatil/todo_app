from flask import Flask
from routes import todo_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(todo_bp)

if __name__ == '__main__':
    app.run(debug=True)
