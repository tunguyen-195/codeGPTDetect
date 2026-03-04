"""
Initialize T07GPTcodeDetect Database
Creates all tables, admin user, demo users and demo analysis data
"""

import sys
import random
from pathlib import Path
from datetime import datetime, timedelta

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


DEMO_USERS = [
    {"email": "nam@t07.com",     "username": "nam",     "full_name": "Nguyen Van Nam",   "role": "user"},
    {"email": "linh@t07.com",    "username": "linh",    "full_name": "Tran Thi Linh",    "role": "user"},
    {"email": "hung@t07.com",    "username": "hung",    "full_name": "Le Van Hung",      "role": "user"},
    {"email": "mai@t07.com",     "username": "mai",     "full_name": "Pham Thi Mai",     "role": "user"},
    {"email": "teacher@t07.com", "username": "teacher", "full_name": "Giang Vien T07",   "role": "admin"},
]

DEMO_PYTHON_AI = """import heapq
from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        min_heap = []
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        return min_heap[0]
"""

DEMO_PYTHON_HUMAN = """def parse_config(filepath):
    config = {}
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return config
"""

DEMO_JAVA_AI = """import java.util.*;
public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
"""

DEMO_JAVA_HUMAN = """public class UserSession {
    private String token;
    private long expiry;

    public UserSession(String token, int ttlSeconds) {
        this.token = token;
        this.expiry = System.currentTimeMillis() + ttlSeconds * 1000L;
    }

    public boolean isExpired() {
        return System.currentTimeMillis() > expiry;
    }

    public String getToken() { return token; }
}
"""

DEMO_ANALYSES = [
    {"code": DEMO_PYTHON_AI,    "language": "python", "model": "python", "prediction": "AI-Generated",  "confidence": 0.9321, "probs": {"AI-Generated": 0.9321, "Human-Written": 0.0679}},
    {"code": DEMO_PYTHON_HUMAN, "language": "python", "model": "python", "prediction": "Human-Written", "confidence": 0.8712, "probs": {"AI-Generated": 0.1288, "Human-Written": 0.8712}},
    {"code": DEMO_JAVA_AI,      "language": "java",   "model": "java",   "prediction": "AI-Generated",  "confidence": 0.8845, "probs": {"AI-Generated": 0.8845, "Human-Written": 0.1155}},
    {"code": DEMO_JAVA_HUMAN,   "language": "java",   "model": "java",   "prediction": "Human-Written", "confidence": 0.9103, "probs": {"AI-Generated": 0.0897, "Human-Written": 0.9103}},
    {"code": DEMO_PYTHON_AI,    "language": "python", "model": "python", "prediction": "AI-Generated",  "confidence": 0.9567, "probs": {"AI-Generated": 0.9567, "Human-Written": 0.0433}},
    {"code": DEMO_PYTHON_HUMAN, "language": "python", "model": "python", "prediction": "Human-Written", "confidence": 0.8234, "probs": {"AI-Generated": 0.1766, "Human-Written": 0.8234}},
    {"code": DEMO_JAVA_AI,      "language": "java",   "model": "java",   "prediction": "AI-Generated",  "confidence": 0.9012, "probs": {"AI-Generated": 0.9012, "Human-Written": 0.0988}},
    {"code": DEMO_JAVA_HUMAN,   "language": "java",   "model": "java",   "prediction": "Human-Written", "confidence": 0.8678, "probs": {"AI-Generated": 0.1322, "Human-Written": 0.8678}},
    {"code": DEMO_PYTHON_AI,    "language": "python", "model": "python", "prediction": "AI-Generated",  "confidence": 0.9789, "probs": {"AI-Generated": 0.9789, "Human-Written": 0.0211}},
    {"code": DEMO_PYTHON_HUMAN, "language": "python", "model": "python", "prediction": "Human-Written", "confidence": 0.9045, "probs": {"AI-Generated": 0.0955, "Human-Written": 0.9045}},
    {"code": DEMO_JAVA_AI,      "language": "java",   "model": "java",   "prediction": "AI-Generated",  "confidence": 0.8523, "probs": {"AI-Generated": 0.8523, "Human-Written": 0.1477}},
    {"code": DEMO_JAVA_HUMAN,   "language": "java",   "model": "java",   "prediction": "Human-Written", "confidence": 0.9234, "probs": {"AI-Generated": 0.0766, "Human-Written": 0.9234}},
]


def init_database():
    """Create all tables, admin user and demo data"""

    print("\n" + "="*70)
    print("T07GPTcodeDetect v3.0 - Database Initialization")
    print("="*70)

    # Create all tables
    print("\n[*] Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Tables created: users, analysis_history, sessions, api_keys, audit_logs")
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    db = SessionLocal()
    try:
        # ---- Admin user ----
        existing_admin = db.query(User).filter(
            (User.email == settings.ADMIN_EMAIL) | (User.username == settings.ADMIN_USERNAME)
        ).first()

        if existing_admin:
            print(f"\n[!] Admin already exists: {existing_admin.email}")
            admin = existing_admin
        else:
            print("\n[*] Creating admin user...")
            admin = User(
                email=settings.ADMIN_EMAIL,
                username=settings.ADMIN_USERNAME,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                full_name="System Administrator",
                role="admin",
                is_active=True,
                is_verified=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"[OK] Admin: {admin.email} / password: {settings.ADMIN_PASSWORD}")

        # ---- Demo users ----
        print("\n[*] Creating demo users...")
        demo_user_ids = [admin.id]
        for u in DEMO_USERS:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if existing:
                demo_user_ids.append(existing.id)
                print(f"    [skip] {u['email']} already exists")
                continue
            user = User(
                email=u["email"],
                username=u["username"],
                full_name=u["full_name"],
                password_hash=get_password_hash("a"),
                role=u["role"],
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            demo_user_ids.append(user.id)
            print(f"    [OK] {user.email} ({user.role})")

        # ---- Demo analyses ----
        existing_count = db.query(AnalysisHistory).count()
        if existing_count > 0:
            print(f"\n[!] Analysis data already exists ({existing_count} records), skipping")
        else:
            print("\n[*] Seeding demo analysis records...")
            base_time = datetime.now() - timedelta(days=7)
            for i, a in enumerate(DEMO_ANALYSES):
                uid = demo_user_ids[i % len(demo_user_ids)]
                created = base_time + timedelta(hours=i * 5 + random.randint(0, 4))
                record = AnalysisHistory(
                    user_id=uid,
                    code=a["code"],
                    language=a["language"],
                    model_used=a["model"],
                    prediction=a["prediction"],
                    confidence=a["confidence"],
                    probabilities=a["probs"],
                    execution_time=round(random.uniform(0.8, 2.5), 3),
                    file_size=len(a["code"]),
                )
                db.add(record)
            db.commit()
            print(f"[OK] Added {len(DEMO_ANALYSES)} demo analysis records")

        # ---- Summary ----
        user_count = db.query(User).count()
        analysis_count = db.query(AnalysisHistory).count()
        print(f"\n[OK] Database ready: {user_count} users, {analysis_count} analyses")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        return False
    finally:
        db.close()

    print("\n" + "="*70)
    print("[OK] Done! Start server: start.bat")
    print(f"     Login: {settings.ADMIN_EMAIL} / {settings.ADMIN_PASSWORD}")
    print("="*70 + "\n")
    return True


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
