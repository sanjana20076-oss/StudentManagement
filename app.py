
from flask import request, jsonify
from database import get_db
import os
from flask import Flask, render_template
from database import init_db
from registration import registration_bp
#from login import login_bp
#from management import management_bp

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "classroom-demo-only-secret"
)

app.register_blueprint(registration_bp)
#app.register_blueprint(login_bp)
#app.register_blueprint(management_bp)


@app.route("/")
def home():
    return render_template("index.html")


init_db()

@app.route("/search")
def search_students():
    name = request.args.get("name", "").strip()

    conn = get_db()
    students = conn.execute(
        """
        SELECT id, name, email, department
        FROM students
        WHERE name LIKE ?
        """,
        (f"%{name}%",)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(debug=True)
