#!/usr/bin/python3
"""
App initialzation and set up
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handles 4o4 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database session after each request"""
    storage.close()


if __name__ == '__main__':
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
