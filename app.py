from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from index import process_resume  # Importing your existing logic

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    # Handle file upload
    file = request.files.get("resume")
    difficulty = request.headers.get("difficulty", "Medium")

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Only .pdf, .jpg or .jpeg files are supported!"}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Process the resume and generate questions
    try:
        questions = process_resume(file_path, difficulty)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)  # Clean up uploaded file

    return jsonify({"questions": questions})


if __name__ == "__main__":
    app.run(debug=True)
