from flask import jsonify


def problem(status, title, detail, error_type=None, errors=None):
    body = {
        "type": error_type or f"urn:problem:{status}",
        "title": title,
        "status": status,
        "detail": detail
    }

    if errors is not None:
        body["errors"] = errors

    return body


def fail(problem_body):
    response = jsonify(problem_body)
    response.status_code = problem_body["status"]
    response.content_type = "application/problem+json"
    return response