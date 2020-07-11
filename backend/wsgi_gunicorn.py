from app.factory import create_app, create_socketio
from app.utils.core import db

app = create_app(config_name="PRODUCTION")
app.app_context().push()


@app.before_first_request
def create_tables():
    db.create_all()


socketio_app = create_socketio(app)
