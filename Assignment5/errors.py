from flask import jsonify

def problem(status, title, detail):
    return {"type": f"https://httpstatuses.com/{status}",
            "title": title, "status": status, "detail": detail}

def fail(p):
    return jsonify(p), p["status"]
