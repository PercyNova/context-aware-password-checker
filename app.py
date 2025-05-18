import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from strength_checker import check_website_password
import pyotp
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))  # For session management

# In-memory store for demo purposes (would use a database in production)
# This should be replaced with actual database storage in production
users_db = {}
temp_totp_storage = {}

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

@app.route("/setup_totp", methods=["POST"])
def setup_totp():
    try:
        data = request.get_json()
        email = data.get("email", "")
        app_name = data.get("app_name", "YourApp")
        
        # Generate a random secret
        secret = pyotp.random_base32()
        
        # Create the OTP auth URL for QR code
        totp = pyotp.TOTP(secret)
        otpauth_url = totp.provisioning_uri(name=email, issuer_name=app_name)
        
        # Store the secret temporarily (would be in a database in production)
        user_id = hash(email)  # Simple user ID for demo
        temp_totp_storage[user_id] = {
            "secret": secret,
            "email": email
        }
        
        return jsonify({
            "success": True,
            "secret": secret,
            "otpauth_url": otpauth_url
        })
    except Exception as e:
        print(f"Error in setup_totp: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/verify_totp", methods=["POST"])
def verify_totp():
    try:
        data = request.get_json()
        secret = data.get("secret", "")
        code = data.get("code", "")
        
        # Create TOTP object
        totp = pyotp.TOTP(secret)
        
        # Verify the code
        is_valid = totp.verify(code)
        
        return jsonify({
            "valid": is_valid
        })
    except Exception as e:
        print(f"Error in verify_totp: {str(e)}")
        return jsonify({
            "valid": False,
            "error": str(e)
        }), 500

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email", "")
        auth_method = data.get("auth_method", "password")
        
        # Create a user ID (in production, this would be a database ID)
        user_id = hash(email)
        
        # Store user data
        users_db[user_id] = {
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "email": email,
            "phone": data.get("phone", ""),
            "address": data.get("address", ""),
            "auth_method": auth_method
        }
        
        # Handle authentication method specific data
        if auth_method == "password":
            users_db[user_id]["password"] = data.get("password", "")
        elif auth_method == "totp":
            users_db[user_id]["totp_secret"] = data.get("totp_secret", "")
        
        return jsonify({
            "success": True,
            "user_id": user_id
        })
    except Exception as e:
        print(f"Error in register: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/totp_verify")
def totp_verify_page():
    user_id = request.args.get("user_id")
    if not user_id or int(user_id) not in users_db:
        return redirect(url_for("index"))
    
    return render_template("totp_verify.html", user_id=user_id)

@app.route("/verify_login_totp", methods=["POST"])
def verify_login_totp():
    try:
        data = request.get_json()
        user_id = int(data.get("user_id", 0))
        code = data.get("code", "")
        
        if user_id not in users_db:
            return jsonify({"success": False, "error": "User not found"})
        
        user = users_db[user_id]
        if user["auth_method"] != "totp":
            return jsonify({"success": False, "error": "User does not use TOTP authentication"})
        
        # Create TOTP object and verify
        totp = pyotp.TOTP(user["totp_secret"])
        is_valid = totp.verify(code)
        
        if is_valid:
            # Set up session for the user
            session["user_id"] = user_id
            session["authenticated"] = True
            
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Invalid code"})
    except Exception as e:
        print(f"Error in verify_login_totp: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
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
