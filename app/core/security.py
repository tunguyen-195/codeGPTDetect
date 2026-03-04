"""
Security utilities
JWT tokens, password hashing, authentication
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt

from app.config import settings

# Using bcrypt directly instead of passlib for compatibility
def _hash_password_bcrypt(password: str) -> str:
    """Hash password using bcrypt directly"""
    # Truncate to 72 bytes if needed
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def _verify_password_bcrypt(password: str, hashed: str) -> bool:
    """Verify password using bcrypt directly"""
    password_bytes = password.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against hashed password"""
    return _verify_password_bcrypt(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return _hash_password_bcrypt(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Payload data (should include 'sub' for user ID)
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Payload data (should include 'sub' for user ID)
        
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Get token payload without verifying (for debugging)
    
    Args:
        token: JWT token
        
    Returns:
        Decoded payload (unverified)
    """
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except JWTError:
        return None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        (is_valid, error_message)
    """
    # Minimum 1 character for development/demo purposes
    if len(password) < 1:
        return False, "Password must be at least 1 character long"
    
    # For production, uncomment these validations:
    # if len(password) < 8:
    #     return False, "Password must be at least 8 characters long"
    # if not any(c.isupper() for c in password):
    #     return False, "Password must contain at least one uppercase letter"
    # if not any(c.islower() for c in password):
    #     return False, "Password must contain at least one lowercase letter"
    # if not any(c.isdigit() for c in password):
    #     return False, "Password must contain at least one digit"
    
    return True, "Password is valid"
