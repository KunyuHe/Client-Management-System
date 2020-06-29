from app.factory import create_app, create_socketio
from app.utils.core import db

app = create_app(config_name="DEVELOPMENT")
app.app_context().push()


@app.before_first_request
def create_tables():
    db.create_all()


socketio = create_socketio(app)

if __name__ == "__main__":
    print(app.url_map)
    socketio.run(app, host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5000, debug=True)
