"""
Initialize T07GPTcodeDetect Database
Creates all tables and admin user
"""

import sys
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
from app.config import settings


def init_database():
    """Create all tables and admin user"""
    
    print("\n" + "="*70)
    print("T07GPTcodeDetect v3.0 - Database Initialization")
    print("He thong phat hien code duoc sinh boi cac mo hinh ngon ngu lon T07")
    print("="*70)
    
    # Create all tables
    print("\n[*] Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Database tables created successfully!")
        print("   - users")
        print("   - analysis_history")
        print("   - sessions")
        print("   - api_keys")
        print("   - audit_logs")
    except Exception as e:
        print(f"[ERROR] Error creating tables: {e}")
        return False
    
    # Create admin user
    db = SessionLocal()
    try:
        # Check if admin exists (by email or username)
        existing_admin = db.query(User).filter(
            (User.email == settings.ADMIN_EMAIL) | (User.username == settings.ADMIN_USERNAME)
        ).first()
        
        if existing_admin:
            print(f"\n[!] Admin user already exists!")
            print(f"   Email: {existing_admin.email}")
            print(f"   Username: {existing_admin.username}")
            print(f"   Role: {existing_admin.role}")
        else:
            print("\n[*] Creating admin user...")
            admin = User(
                email=settings.ADMIN_EMAIL,
                username=settings.ADMIN_USERNAME,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                full_name="System Administrator",
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            
            print(f"[OK] Admin user created successfully!")
            print(f"   Email: {admin.email}")
            print(f"   Username: {admin.username}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
            print(f"   Role: {admin.role}")
            print(f"\n[!] [!] [!] IMPORTANT: CHANGE PASSWORD AFTER FIRST LOGIN!  [!] [!] [!]")
    
    except Exception as e:
        print(f"\n[ERROR] Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    # Verify database
    print("\n[*] Verifying database...")
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        print(f"[OK] Database verification successful!")
        print(f"   Total users: {user_count}")
    except Exception as e:
        print(f"[ERROR] Database verification failed: {e}")
        return False
    finally:
        db.close()
    
    print("\n" + "="*70)
    print("[OK] Database initialization complete!")
    print("="*70)
    print("\nNext steps:")
    print("   1. Start the server: python app/main.py")
    print("   2. Open browser: http://localhost:8000")
    print("   3. Login with admin credentials:")
    print(f"      Email: {settings.ADMIN_EMAIL}")
    print(f"      Password: {settings.ADMIN_PASSWORD}")
    print("   4. [!] Change admin password in settings!")
    print("\n" + "="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
