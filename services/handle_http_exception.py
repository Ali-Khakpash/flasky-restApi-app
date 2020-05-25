from flask import jsonify


def handle_http_exception(e):
    if e.code == 413:
        return jsonify(status_code=e.code, description=e.description)
    elif e.code == 404:
        return jsonify(status_code=e.code, description=e.description)
    else:
        return jsonify(status_code=500, description=e.description)
    pass
