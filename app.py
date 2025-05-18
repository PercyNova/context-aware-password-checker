import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from strength_checker import check_website_password

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check_password", methods=["POST"])
def check_password():
    try:
        data = request.get_json()
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        
        strength, feedback = check_website_password(password, first_name, last_name, email)
        
        return jsonify({
            "strength": strength,
            "feedback": feedback
        })
    except Exception as e:
        # Log the error (in a production app you'd use proper logging)
        print(f"Error in check_password: {str(e)}")
        return jsonify({
            "strength": "Error",
            "feedback": ["An error occurred while checking password strength."]
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Internal server error"), 500

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5000))
    
    # In production, you should set debug to False
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(host='0.0.0.0', port=port, debug=debug)