"""
Reset T07GPTcodeDetect Database
Deletes old database and creates new one with default accounts
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.analysis import AnalysisHistory
from app.models.session import Session as SessionModel
from app.models.api_key import APIKey
from app.models.audit_log import AuditLog
from app.core.security import get_password_hash


# Default accounts with password "a"
DEFAULT_ACCOUNTS = [
    {
        "email": "admin@t07.com",
        "username": "admin",
        "password": "a",
        "full_name": "System Administrator",
        "role": "admin"
    },
    {
        "email": "user1@t07.com",
        "username": "user1",
        "password": "a",
        "full_name": "User 1",
        "role": "user"
    },
    {
        "email": "user2@t07.com",
        "username": "user2",
        "password": "a",
        "full_name": "User 2",
        "role": "user"
    },
    {
        "email": "demo@t07.com",
        "username": "demo",
        "password": "a",
        "full_name": "Demo User",
        "role": "user"
    }
]


def reset_database():
    """Delete and recreate database with default accounts"""
    
    print("\n" + "="*70)
    print("T07GPTcodeDetect v3.0 - Database Reset")
    print("="*70)
    
    # Get database path
    project_root = Path(__file__).parent.parent
    db_path = project_root / "t07gptcodedetect.db"
    
    # Delete existing database
    if db_path.exists():
        print(f"\n[*] Deleting existing database: {db_path}")
        try:
            os.remove(db_path)
            print("[OK] Old database deleted!")
        except Exception as e:
            print(f"[ERROR] Failed to delete database: {e}")
            print("[!] Please close any applications using the database and try again.")
            return False
    
    # Create all tables
    print("\n[*] Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Database tables created!")
        print("   - users")
        print("   - analysis_history")
        print("   - sessions")
        print("   - api_keys")
        print("   - audit_logs")
    except Exception as e:
        print(f"[ERROR] Error creating tables: {e}")
        return False
    
    # Create default accounts
    print("\n[*] Creating default accounts...")
    db = SessionLocal()
    try:
        for account in DEFAULT_ACCOUNTS:
            user = User(
                email=account["email"],
                username=account["username"],
                password_hash=get_password_hash(account["password"]),
                full_name=account["full_name"],
                role=account["role"],
                is_active=True,
                is_verified=True
            )
            db.add(user)
            print(f"   [+] {account['email']} ({account['role']})")
        
        db.commit()
        print(f"\n[OK] Created {len(DEFAULT_ACCOUNTS)} accounts!")
        
    except Exception as e:
        print(f"\n[ERROR] Error creating accounts: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    # Summary
    print("\n" + "="*70)
    print("[OK] Database reset complete!")
    print("="*70)
    print("\nDefault Accounts (all passwords = 'a'):")
    print("-"*50)
    for account in DEFAULT_ACCOUNTS:
        print(f"  Email: {account['email']:<25} Role: {account['role']}")
    print("-"*50)
    print("\nTo start the server:")
    print("  python -m app.main")
    print("  OR")
    print("  start.bat")
    print("\n" + "="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1)
