# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, make_response, request, send_from_directory, session

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "change-this-secret-key-for-demo"

# In-memory data for teaching. Restarting the server resets this list.
study_sessions = [
    {"id": 1, "topic": "Understand GET requests", "minutes": 25, "completed": False},
    {"id": 2, "topic": "Practice Flask routes", "minutes": 30, "completed": False},
]


def find_study_session(session_id):
    for item in study_sessions:
        if item["id"] == session_id:
            return item
    return None


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/me", methods=["GET"])
def get_current_user():
    """Show how session and cookie data can persist across requests."""
    session["visits"] = session.get("visits", 0) + 1
    return jsonify(
        {
            "username": session.get("username"),
            "visits": session["visits"],
            "focus_mode": request.cookies.get("focus_mode", "standard"),
        }
    )


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "Username is required."}), 400

    session["username"] = username
    session["visits"] = 0
    return jsonify({"message": "Login successful", "username": username}), 201


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Session cleared. You are logged out."})


@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions():
    return jsonify(study_sessions)


@app.route("/api/study-sessions", methods=["POST"])
def create_study_session():
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()
    minutes = data.get("minutes", 25)

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    try:
        minutes = int(minutes)
    except (TypeError, ValueError):
        return jsonify({"error": "Minutes must be a number."}), 400

    new_item = {
        "id": max([item["id"] for item in study_sessions], default=0) + 1,
        "topic": topic,
        "minutes": minutes,
        "completed": False,
    }
    study_sessions.append(new_item)
    return jsonify(new_item), 201


@app.route("/api/study-sessions/<int:session_id>", methods=["PATCH"])
def complete_study_session(session_id):
    item = find_study_session(session_id)

    if item is None:
        return jsonify({"error": "Study session not found."}), 404

    item["completed"] = True
    return jsonify(item)


@app.route("/api/study-sessions/<int:session_id>", methods=["DELETE"])
def delete_study_session(session_id):
    item = find_study_session(session_id)

    if item is None:
        return jsonify({"error": "Study session not found."}), 404

    study_sessions.remove(item)
    return jsonify({"message": "Study session deleted.", "deleted": item})


@app.route("/api/focus-mode", methods=["POST"])
def set_focus_mode():
    data = request.get_json() or {}
    mode = data.get("mode", "standard")
    allowed_modes = {"standard", "deep", "revision", "practice"}

    if mode not in allowed_modes:
        return jsonify({"error": "Invalid focus mode."}), 400

    response = make_response(jsonify({"message": "Focus mode saved.", "focus_mode": mode}))
    response.set_cookie("focus_mode", mode, max_age=60 * 60 * 24 * 7, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
