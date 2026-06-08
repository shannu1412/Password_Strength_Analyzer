import re
import hashlib
import sqlite3
from typing import Tuple, List, Optional

class PasswordStrengthAnalyzer:
    def __init__(self, use_database: bool = True, db_path: str = "password_history.db"):
        self.common_passwords = self._load_common_passwords()
        self.use_database = use_database
        self.db_path = db_path
        self.connection = None
        self._init_db()

    def _load_common_passwords(self) -> set:
        return {
            "password", "123456", "12345678", "123456789", "qwerty",
            "abc123", "password123", "admin", "iloveyou", "welcome",
            "monkey", "dragon", "sunshine", "passw0rd", "letmein",
            "football", "baseball", "michael", "jordan", "shadow",
            "master", "hello", "freeman", "whatever", "trustno1"
        }

    def _init_db(self):
        if not self.use_database:
            return
            
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
        except Exception as e:
            print(f"Note: Using in-memory database (file-based DB failed: {e})")
            self.connection = sqlite3.connect(":memory:")
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _is_password_used_before(self, password: str) -> bool:
        if not self.use_database or not self.connection:
            return False
            
        try:
            password_hash = self._hash_password(password)
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1 FROM password_history WHERE password_hash = ?", (password_hash,))
            exists = cursor.fetchone() is not None
            return exists
        except Exception:
            return False

    def store_old_password(self, password: str):
        if not self.use_database or not self.connection:
            print("Database not available — password reuse tracking disabled")
            return
            
        try:
            password_hash = self._hash_password(password)
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO password_history (password_hash) VALUES (?)", (password_hash,))
            self.connection.commit()
            print("✓ Password stored in history")
        except Exception as e:
            print(f"Could not store password: {e}")

    def evaluate(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []

        length = len(password)
        if length >= 12:
            score += 30
        elif length >= 8:
            score += 20
            issues.append(f"Length is {length} characters — 12+ is better")
            suggestions.append("Increase length to at least 12 characters")
        else:
            issues.append(f"Length is only {length} characters — too short")
            suggestions.append("Use at least 12 characters")

        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        complexity_score = 0
        if has_lower:
            complexity_score += 5
        if has_upper:
            complexity_score += 10
        if has_digit:
            complexity_score += 10
        if has_special:
            complexity_score += 15

        score += complexity_score

        if not has_upper:
            issues.append("No uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
        if not has_digit:
            issues.append("No digits")
            suggestions.append("Add numbers (0-9)")
        if not has_special:
            issues.append("No special characters")
            suggestions.append("Add special characters (!@#$%^&*)")

        if password.lower() in self.common_passwords:
            issues.append("This is a very common password")
            suggestions.append("Avoid common passwords like 'password', '123456', etc.")
            score = max(0, score - 30)

        if re.search(r'(.)\1{2,}', password):
            issues.append("Contains repeated characters (e.g., 'aaa')")
            suggestions.append("Avoid repeating the same character many times")

        if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
            issues.append("Contains easy sequential pattern")
            suggestions.append("Avoid sequential letters or numbers")
            
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn', 'qwertyuiop', 'asdfghjkl']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                issues.append("Contains keyboard pattern (e.g., 'qwerty')")
                suggestions.append("Avoid keyboard sequences")
                score = max(0, score - 20)
                break

        if self._is_password_used_before(password):
            issues.append("You have used this password before")
            suggestions.append("Choose a password you haven't used recently")

        score = min(100, max(0, score))

        if score >= 80:
            suggestions.append("Great! Consider using a passphrase (e.g., correct-horse-battery-staple)")
        
        if score < 30:
            suggestions.append("⚠️ Consider using a password manager to generate strong unique passwords")

        return score, issues, suggestions

    def suggest_strong_passwords(self, base_password: str, num_suggestions: int = 3) -> List[str]:
        suggestions = []
        
        if len(base_password) < 12:
            suggestions.append(base_password + "Tr0ub4dor&3")
        
        if not re.search(r'[!@#$]', base_password):
            suggestions.append(base_password.capitalize() + "@" + str(abs(hash(base_password)) % 100))
        
        common_words = ["Tiger", "Moon", "Sky", "Frog", "Blue", "Star", "Coffee", "Piano", "Ocean", "Forest"]
        import random
        random.seed(abs(hash(base_password)) % 1000)
        word1 = random.choice(common_words)
        word2 = random.choice(common_words)
        word3 = random.choice(common_words)
        num = random.randint(10, 99)
        suggestion = f"{word1}-{word2}-{word3}{num}!"
        suggestions.append(suggestion)
        
        score, _, _ = self.evaluate(base_password)
        if score < 40:
            suggestions.append("CorrectHorse-BatteryStaple-2024!")

        suggestions = list(dict.fromkeys(suggestions))
        return suggestions[:num_suggestions]