#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    storage.close()

if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port)

