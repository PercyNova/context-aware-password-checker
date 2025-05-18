# context-aware-password-checker

A secure and context-aware password strength checker application built with Flask. This application provides real-time feedback on password strength and detects when users try to include personal information in their passwords.

## Features

- **Real-time password strength analysis** with visual feedback
- **Context-aware validation** that prevents users from including personal information in passwords
- **Leetspeak detection** that identifies when users try to bypass filters using number/symbol substitutions
- **Password entropy calculation** for accurate security measurement
- **Common password blacklist** checking against known vulnerable passwords
- **Client-side validation** for basic requirements (length, character types)
- **Password confirmation** to prevent typos during registration

## Technical Overview

This application consists of three main components:

1. **Backend API (Flask)** - Handles password strength calculations and context-aware validation
2. **Strength Checker Engine** - Analyzes passwords against multiple security criteria  
3. **Frontend Interface** - Provides real-time feedback and visual indicators

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-strength-checker.git
   cd password-strength-checker
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

4. Add the password blacklist file:
   - Download the `rockyou.txt` wordlist (or another password dictionary)
   - Place it in the project root directory
   - Note: If you don't have access to `rockyou.txt`, the application will still work but with reduced blacklist checking capabilities

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Configuration

The password strength criteria can be adjusted in the `strength_checker.py` file:

- Modify entropy thresholds for different strength levels
- Add or remove common patterns to check against
- Customize feedback messages for different validation checks

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

#### Render

1. Create an account on [render.com](https://render.com/)
2. Connect your GitHub repository
3. Create a new Web Service with these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Integrating with an Existing Website

To add this password checker to your existing website:

1. Include the backend files:
   - `app.py` (adapt the routes to your existing backend)
   - `strength_checker.py`
   
2. Add the form HTML to your website page and update the API endpoint in the JavaScript

3. Include the CSS styles from the `index.html` file

## How It Works

### Password Strength Checking

The application uses multiple criteria to evaluate password strength:

1. **Length** - Longer passwords are generally stronger
2. **Character variety** - Mix of uppercase, lowercase, numbers, and symbols
3. **Entropy calculation** - Mathematical measurement of randomness
4. **Pattern detection** - Checks for common patterns and sequences
5. **Blacklist checking** - Compares against known common passwords
6. **Personal information detection** - Ensures passwords don't contain user details

### Context-Aware Validation

The application checks if passwords contain:
- First name
- Last name
- Email username
- Variations using leetspeak substitutions (e.g., replacing 'a' with '@' or '4')

## Security Notes

- This application is designed to enhance password security but should be part of a larger security strategy
- Always use HTTPS in production to protect password data in transit
- Consider adding rate limiting to prevent brute force attacks
- The application does not store passwords; it only evaluates their strength

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Password strength calculation inspired by NIST guidelines
- Entropy calculation methodology based on information theory principles
- Leetspeak detection patterns from common substitution practices

## Future Improvements

- Add more sophisticated pattern recognition
- Implement machine learning for better password strength prediction
- Support for multiple languages and internationalization
- Additional visualization options for password strength metrics
