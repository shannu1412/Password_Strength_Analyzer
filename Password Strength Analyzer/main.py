from password_strength_analyzer import PasswordStrengthAnalyzer
import re

def main():
    print("=" * 50)
    print("     Password Strength Analyzer")
    print("=" * 50)
    print("\n📌 Tip: Strong passwords have:")
    print("   • 12+ characters")
    print("   • Uppercase & lowercase letters")
    print("   • Numbers & special characters")
    print("   • No common patterns or words")
    print("-" * 50)
    
    try:
        analyzer = PasswordStrengthAnalyzer(use_database=True)
    except Exception:
        print("⚠️ Running in limited mode (password history disabled)\n")
        analyzer = PasswordStrengthAnalyzer(use_database=False)
    
    password_history_enabled = analyzer.use_database and analyzer.connection is not None
    
    while True:
        print("\n" + "=" * 50)
        print("MENU:")
        print("  1. 🔍 Analyze a password")
        print("  2. 💡 Get password suggestions only")
        if password_history_enabled:
            print("  3. 🗑️  Clear password history")
        print("  4. 🚪 Exit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "4":
            break
        
        elif choice == "2":
            print("\n💡 PASSWORD SUGGESTIONS (examples):")
            print("   • Use a phrase: 'MyCatLovesTunaFish!'")
            print("   • Mix cases: 'SuMmEr2024@Beach'")
            print("   • Random words: 'Tiger$ky88!Bridge'")
            print("   • Length is king — 16+ chars is excellent")
            continue
            
        elif choice == "3" and password_history_enabled:
            confirm = input("Clear all stored password history? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    cursor = analyzer.connection.cursor()
                    cursor.execute("DELETE FROM password_history")
                    analyzer.connection.commit()
                    print("✓ Password history cleared")
                except Exception as e:
                    print(f"Error clearing history: {e}")
            continue
        
        elif choice != "1":
            print("Invalid choice. Please try again.")
            continue
        
        password = input("\nEnter password to analyze: ").strip()
        if not password:
            print("❌ Password cannot be empty.")
            continue
        
        if len(password) > 100:
            print("⚠️ Password is very long — analysis may be slower")
        
        score, issues, suggestions = analyzer.evaluate(password)
        
        print("\n" + "=" * 50)
        print(f"📊 STRENGTH SCORE: {score}/100")
        
        if score >= 80:
            print("🟢 Verdict: EXCELLENT — Strong password")
            bar = "████████████████████"
        elif score >= 65:
            print("🟡 Verdict: GOOD — Could be slightly better")
            bar = "███████████████░░░░░"
        elif score >= 45:
            print("🟠 Verdict: FAIR — Consider improvements")
            bar = "██████████░░░░░░░░░░"
        else:
            print("🔴 Verdict: WEAK — Change immediately!")
            bar = "█████░░░░░░░░░░░░░░░"
        
        print(f"[{bar}]")
        
        if issues:
            print("\n🔻 ISSUES FOUND:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
        
        if suggestions:
            print("\n💡 IMPROVEMENT SUGGESTIONS:")
            for i, sug in enumerate(suggestions, 1):
                print(f"   {i}. {sug}")
        
        print("\n📈 DETAILS:")
        print(f"   • Length: {len(password)} characters")
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        print(f"   • Uppercase: {'✅' if has_upper else '❌'}")
        print(f"   • Lowercase: {'✅' if has_lower else '❌'}")
        print(f"   • Numbers: {'✅' if has_digit else '❌'}")
        print(f"   • Special chars: {'✅' if has_special else '❌'}")
        
        if score < 80:
            gen = input("\n🔧 Generate stronger password examples? (y/n): ").strip().lower()
            if gen == 'y':
                strong_sugs = analyzer.suggest_strong_passwords(password)
                print("\n🔐 STRONGER PASSWORD EXAMPLES (DO NOT COPY BLINDLY):")
                for i, sug in enumerate(strong_sugs, 1):
                    print(f"   {i}. {sug}")
                print("\n   ⚠️ Always create your own unique password")
        
        if password_history_enabled and score >= 50:
            store = input("\n💾 Store this password to prevent reuse later? (y/n): ").strip().lower()
            if store == 'y':
                analyzer.store_old_password(password)
    
    print("\n" + "=" * 50)
    print("👋 Stay secure! Remember: Never share your passwords.")
    print("=" * 50)

if __name__ == "__main__":
    main()