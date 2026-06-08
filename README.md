# Password Strength Analyzer

## Project Overview

The **Password Strength Analyzer** is a security tool that evaluates password strength in real-time, helping users create stronger, more secure passwords. It analyzes passwords based on multiple security criteria and provides actionable feedback with specific improvement suggestions.

## Core Functionality

This tool examines passwords against several security metrics:

1. **Length** – Checks if the password meets minimum security standards (8+ characters, with 12+ recommended)

2. **Character Complexity** – Verifies the presence of:
   - Uppercase letters (A-Z)
   - Lowercase letters (a-z)
   - Numeric digits (0-9)
   - Special characters (!@#$%^&* etc.)

3. **Pattern Detection** – Identifies weak patterns including:
   - Sequential characters (123, abc, 789)
   - Repeated characters (aaa, 111, zzz)
   - Keyboard walking patterns (qwerty, asdfgh)

4. **Common Password Check** – Compares against a list of frequently used weak passwords

5. **Reuse Prevention** – Stores hashed passwords (SHA-256) in a local database to prevent reuse

## Output & Feedback

The tool provides:
- A numerical strength score (0-100)
- Visual progress bar
- List of specific issues found
- Actionable improvement suggestions
- Stronger password alternatives

## Technical Implementation

- **Language:** Python 3.6+
- **Cryptography:** SHA-256 hashing (hashlib)
- **Database:** SQLite3 for password history
- **Pattern Matching:** Regular expressions (re module)

## Use Cases

- Security awareness training
- Password policy enforcement
- Educational demonstrations
- Registration system integration

## Learning Outcomes

This project demonstrates proficiency in:
- Password security best practices
- Cryptographic hashing concepts
- Pattern detection algorithms
- Database integration for security features
- Error handling in restricted environments

## Author

Developed as part of the internship program at **Thiranex Technologies**
