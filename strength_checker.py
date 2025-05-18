import math
import string
import re
import os

def load_blacklist(filepath):
    if not os.path.isfile(filepath):
        print(f"Warning: blacklist file {filepath} not found, skipping.")
        return set()
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return set(line.strip() for line in file)

# Get the absolute path to the current directory (where this script is located)
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = 'rockyou.txt'
filepath = os.path.join(script_dir, filename)

BLACKLIST = set()
if os.path.exists(filepath):
    print(f"Loading blacklist file: {filepath}")
    BLACKLIST.update(load_blacklist(filepath))
else:
    print(f"Blacklist file not found: {filepath}")
    # Continue without blacklist - we'll use other security measures


# Leet speak substitutions dictionary
LEET_SUBS = {
    '0': 'o',
    '1': ['i', 'l'],
    '3': 'e',
    '4': 'a',
    '8': 'b',
    '@': 'a',
    '$': 's'
}

def normalize_leetspeak(text):
    """Convert common leetspeak substitutions to normal characters"""
    normalized = text.lower()
    for leet_char, normal_chars in LEET_SUBS.items():
        if isinstance(normal_chars, list):
            for char in normal_chars:
                normalized = normalized.replace(leet_char, char)
        else:
            normalized = normalized.replace(leet_char, normal_chars)
    return normalized

def contains_personal_info(password, personal_info, normalized=False):
    """Check if password contains any personal information"""
    if not password or not personal_info:
        return False

    pwd = normalize_leetspeak(password) if normalized else password.lower()

    for info in personal_info:
        if info and len(info) > 2:  # Only check meaningful personal info
            info = info.lower()
            if info in pwd:
                return True

    return False

def check_password_strength_with_context(password, first_name="", last_name="", email=""):
    """Check password strength with context awareness"""
    feedback = []

    # Check for personal information in the password (both regular and leetspeak)
    personal_info = [first_name, last_name]
    if email and "@" in email:
        username = email.split("@")[0]
        personal_info.append(username)

    # Regular check
    if contains_personal_info(password, personal_info):
        return "Rejected", ["Password contains your personal information. Choose something more private."]

    # Leetspeak check
    if contains_personal_info(password, personal_info, normalized=True):
        return "Rejected", ["Password contains your personal information (using number/symbol substitutions). Choose something more private."]

    # Continue with regular strength checking
    score = 0
    length = len(password)

    if length < 8:
        feedback.append("Password is too short. Use at least 8 characters.")
    elif length >= 12:
        score += 2
        feedback.append("Good length.")
    else:
        score += 1
        feedback.append("Length is acceptable. The longer, the better.")

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    types = [has_lower, has_upper, has_digit, has_symbol]
    type_count = sum(types)
    score += type_count

    if type_count < 3:
        feedback.append("Use a mix of uppercase, lowercase, numbers, and symbols.")
    else:
        feedback.append("Good mix of character types.")

    # Check against common password blacklist
    if password.lower() in BLACKLIST:
        return "Rejected", ["Password is too common or leaked. Try a more unique one."]

    # Check for common patterns
    common_patterns = ['123456', 'password', 'qwerty', 'abc', 'letmein', 'iloveyou', 'admin', 'welcome', 'monkey', '12345']
    if any(p in password.lower() for p in common_patterns):
        feedback.append("Avoid common patterns or sequences.")
        score -= 2

    # Entropy Calculation
    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += len(string.punctuation)

    entropy = length * math.log2(charset_size) if charset_size > 0 else 0


    # Adjusted entropy-based strength classification with lower thresholds
    if entropy < 35:
        strength = "Very Weak"
    elif entropy < 50:
        strength = "Weak"
    elif entropy < 70:
        strength = "Moderate"
    elif entropy < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    # Add specific feedback about avoiding personal information
    feedback.append("Never use your name, surname, or email in your password.")

    return strength, feedback

def check_website_password(password, first_name="", last_name="", email=""):
    """Function specifically designed for website password checking with context awareness"""
    # First, check for the presence of personal information
    if first_name or last_name or email:
        # Direct containment check
        if first_name and first_name.lower() in password.lower():
            return "Rejected", [f"Password contains your first name ({first_name}). Choose something more private."]

        if last_name and last_name.lower() in password.lower():
            return "Rejected", [f"Password contains your last name ({last_name}). Choose something more private."]

        if email and "@" in email:
            username = email.split("@")[0].lower()
            if username in password.lower():
                return "Rejected", [f"Password contains part of your email ({username}). Avoid using personal info."]

        # Leetspeak detection for personal information
        normalized_pwd = normalize_leetspeak(password)

        if first_name and first_name.lower() in normalized_pwd:
            return "Rejected", [f"Password contains your first name with number/symbol substitutions. Choose something more private."]

        if last_name and last_name.lower() in normalized_pwd:
            return "Rejected", [f"Password contains your last name with number/symbol substitutions. Choose something more private."]

        if email and "@" in email:
            username = email.split("@")[0].lower()
            if username in normalized_pwd:
                return "Rejected", [f"Password contains part of your email with number/symbol substitutions. Avoid using personal info."]

    # If no personal info is detected, proceed with standard strength check
    return check_password_strength_with_context(password, first_name, last_name, email)
