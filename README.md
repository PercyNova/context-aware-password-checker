# Context-Aware Authentication System

A secure and context-aware authentication system built with Flask. This application provides real-time feedback on password strength, detects when users try to include personal information in their passwords, and offers two-factor authentication via authenticator apps.

## Features

### Password Authentication
- **Real-time password strength analysis** with visual feedback
- **Context-aware validation** that prevents users from including personal information in passwords
- **Leetspeak detection** that identifies when users try to bypass filters using number/symbol substitutions
- **Password entropy calculation** for accurate security measurement
- **Common password blacklist** checking against known vulnerable passwords
- **Client-side validation** for basic requirements (length, character types)
- **Password confirmation** to prevent typos during registration

### Two-Factor Authentication (2FA)
- **Time-based One-Time Password (TOTP)** support via authenticator apps
- **QR code generation** for easy setup with authenticator apps
- **Manual key provision** for cases where QR scanning isn't possible
- **TOTP verification** to ensure proper setup before account creation
- **Auto-regenerating codes** for enhanced security (expires after 5 minutes of inactivity)

## Technical Overview

This application consists of several main components:

1. **Backend API (Flask)** - Handles authentication methods, password strength calculations, and TOTP generation
2. **Strength Checker Engine** - Analyzes passwords against multiple security criteria
3. **TOTP Implementation** - Generates and validates time-based one-time passwords
4. **Frontend Interface** - Provides real-time feedback, visual indicators, and authentication options

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/context-aware-authentication.git
   cd context-aware-authentication
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add the password blacklist file (optional for enhanced password security):
   - Download the `rockyou.txt` wordlist [rockyou.txt wordlist](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)
   - Place it in the project root directory

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Authentication Options

The application offers two authentication methods:

### 1. Password-Based Authentication
- Traditional password-based login with enhanced security measures
- Real-time strength feedback during password creation
- Protection against personal information inclusion

### 2. Authenticator App (TOTP)
- Password-less authentication using any TOTP-compatible authenticator app
- Supports Google Authenticator, Authy, Microsoft Authenticator, and others
- QR code scanning for quick setup
- Manual key entry option for accessibility

## Configuration

The application can be configured in several ways:

- Password strength criteria in the `strength_checker.py` file
- TOTP settings (expiration time, issuer name) in `app.py`
- Session security settings and secret key in `app.py`

## Deployment

### Deploying to a Cloud Service

#### Heroku

1. Create a `Procfile` in the project root:
   ```
   web: gunicorn app:app
   ```

2. Add `gunicorn` to your requirements:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Security Considerations

- Set a strong `SECRET_KEY` environment variable for production
- Always use HTTPS in production to protect authentication data in transit
- Consider adding rate limiting to prevent brute force attacks
- In production, replace the in-memory storage with a proper database

## How It Works

### Password Authentication Flow

1. User enters personal information and password
2. Client-side validation checks basic requirements
3. Server-side validation provides detailed strength analysis
4. Context-aware checks prevent use of personal information
5. Password is verified against common password lists
6. Entropy calculation determines final strength rating

### TOTP Authentication Flow

1. User enters personal information and selects TOTP authentication
2. Server generates a random secret key
3. QR code is displayed for scanning with authenticator app
4. User verifies setup by entering a generated code
5. Upon verification, account is created with TOTP as authentication method
6. Future logins require a fresh code from the authenticator app

## Security Notes

- TOTP secrets automatically expire after 5 minutes of inactivity
- QR codes are generated client-side using the QRious library
- The application does not store passwords in plaintext
- In production, implement proper database storage for user data

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Improvements

- Add support for additional 2FA methods (SMS, email)
- Implement account recovery options
- Add biometric authentication support for compatible devices
- Support for multiple languages and internationalization
- Enhanced security logging and monitoring
