from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)

from . import backend
app.register_blueprint(backend.api.bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")