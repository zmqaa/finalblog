from app import create_app, db
from flask_migrate import Migrate
from flask import render_template


app = create_app()
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)