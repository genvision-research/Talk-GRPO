from flask import Flask, render_template, send_from_directory
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, template_folder="templates")


def load_data():
    json_path = BASE_DIR / "data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(BASE_DIR / "assets", filename, conditional=True)


@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory(BASE_DIR / "images", filename, conditional=True)


@app.route("/test_videos/<path:filename>")
def serve_test_videos(filename):
    return send_from_directory(BASE_DIR / "test_videos", filename, conditional=True)


@app.route("/qualitative_results/<path:filename>")
def serve_qualitative_results(filename):
    return send_from_directory(BASE_DIR / "qualitative_results", filename, conditional=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)