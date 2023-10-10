from flask_app import app
from flask_app.controllers.users import app
from flask_app.controllers.magazines import app
if __name__ == "__main__":
    app.run(debug=True)