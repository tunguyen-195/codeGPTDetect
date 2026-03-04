"""
Integration tests for GPTSniffer v3.0 API
Tests authentication, users, analysis, and history endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User
from app.core.security import get_password_hash

client = TestClient(app)

# Test data
TEST_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123!@#",
    "full_name": "Test User"
}

TEST_CODE_PYTHON = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

TEST_CODE_JAVA = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_headers():
    """Get authentication headers for testing"""
    # Register user
    client.post("/api/auth/register", json=TEST_USER)
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "app" in response.json()
        assert response.json()["app"] == "GPTSniffer"
    
    def test_health_check(self):
        """Test health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_register_success(self):
        """Test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewPass123!",
            "full_name": "New User"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 201
        assert response.json()["success"] is True
    
    def test_register_duplicate_email(self, auth_headers):
        """Test registration with duplicate email"""
        response = client.post("/api/auth/register", json=TEST_USER)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_login_success(self):
        """Test successful login"""
        response = client.post("/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert "user" in response.json()
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
    
    def test_get_current_user(self, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["email"] == TEST_USER["email"]
        assert response.json()["username"] == TEST_USER["username"]


class TestAnalysisEndpoints:
    """Test code analysis endpoints"""
    
    def test_analyze_python_code(self, auth_headers):
        """Test analyzing Python code"""
        request_data = {
            "code": TEST_CODE_PYTHON,
            "language": "python",
            "model": "python",
            "save_to_history": True
        }
        
        response = client.post("/api/analysis", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        assert "prediction" in response.json()
        assert "confidence" in response.json()
        assert "probabilities" in response.json()
        assert response.json()["language"] == "python"
    
    def test_analyze_java_code(self, auth_headers):
        """Test analyzing Java code"""
        request_data = {
            "code": TEST_CODE_JAVA,
            "language": "java",
            "model": "java",
            "save_to_history": True
        }
        
        response = client.post("/api/analysis", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        assert "prediction" in response.json()
        assert response.json()["language"] == "java"
    
    def test_analyze_auto_detect(self, auth_headers):
        """Test auto language detection"""
        request_data = {
            "code": TEST_CODE_PYTHON,
            "language": "auto",
            "model": "auto",
            "save_to_history": False
        }
        
        response = client.post("/api/analysis", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["language"] in ["python", "java", "cpp"]
    
    def test_get_available_models(self):
        """Test getting available models"""
        response = client.get("/api/analysis/models")
        
        assert response.status_code == 200
        assert "models" in response.json()["data"]
        assert "languages" in response.json()["data"]


class TestHistoryEndpoints:
    """Test analysis history endpoints"""
    
    def test_get_history(self, auth_headers):
        """Test getting analysis history"""
        # First create some analyses
        request_data = {
            "code": TEST_CODE_PYTHON,
            "language": "python",
            "model": "python",
            "save_to_history": True
        }
        client.post("/api/analysis", json=request_data, headers=auth_headers)
        
        # Get history
        response = client.get("/api/history", headers=auth_headers)
        
        assert response.status_code == 200
        assert "analyses" in response.json()
        assert "total" in response.json()
        assert len(response.json()["analyses"]) > 0
    
    def test_get_history_stats(self, auth_headers):
        """Test getting history statistics"""
        response = client.get("/api/history/stats", headers=auth_headers)
        
        assert response.status_code == 200
        assert "total_analyses" in response.json()
        assert "ai_generated" in response.json()
        assert "human_written" in response.json()
    
    def test_delete_history_item(self, auth_headers):
        """Test deleting history item"""
        # Create analysis
        request_data = {
            "code": TEST_CODE_PYTHON,
            "language": "python",
            "save_to_history": True
        }
        response = client.post("/api/analysis", json=request_data, headers=auth_headers)
        analysis_id = response.json()["analysis_id"]
        
        # Delete it
        response = client.delete(f"/api/history/{analysis_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()


class TestUserEndpoints:
    """Test user management endpoints"""
    
    def test_get_my_profile(self, auth_headers):
        """Test getting own profile"""
        response = client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["email"] == TEST_USER["email"]
    
    def test_update_my_profile(self, auth_headers):
        """Test updating own profile"""
        update_data = {
            "full_name": "Updated Name",
            "bio": "Test bio"
        }
        
        response = client.put("/api/users/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["full_name"] == "Updated Name"


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    @pytest.fixture
    def admin_headers(self):
        """Get admin authentication headers"""
        # Create admin user directly in database
        db = SessionLocal()
        try:
            admin = User(
                email="admin@test.com",
                username="admin",
                password_hash=get_password_hash("Admin123!"),
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            db.commit()
        except:
            pass
        finally:
            db.close()
        
        # Login as admin
        response = client.post("/api/auth/login", json={
            "email": "admin@test.com",
            "password": "Admin123!"
        })
        
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_get_system_stats(self, admin_headers):
        """Test getting system statistics"""
        response = client.get("/api/admin/stats", headers=admin_headers)
        
        assert response.status_code == 200
        assert "users" in response.json()["data"]
        assert "analyses" in response.json()["data"]
    
    def test_admin_health_check(self):
        """Test admin health check"""
        response = client.get("/api/admin/health")
        
        assert response.status_code == 200
        assert "status" in response.json()["data"]


def run_tests():
    """Run all tests"""
    print("="*70)
    print("RUNNING INTEGRATION TESTS")
    print("="*70)
    
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
