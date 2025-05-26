# Data models for the authentication API
# Using standard Python classes instead of Pydantic since external packages
# are not supported in Cloudflare Workers Python production deployment

from typing import Optional, Dict, Any

class LoginRequest:
    """Login request data structure"""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LoginRequest':
        """Create LoginRequest from dictionary"""
        username = data.get("username", "")
        password = data.get("password", "")
        
        # Basic validation
        if not username or len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        return cls(username, password)

class LoginResponse:
    """Login response data structure"""
    def __init__(self, access_token: str, token_type: str, user_id: str, username: str):
        self.access_token = access_token
        self.token_type = token_type
        self.user_id = user_id
        self.username = username
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "user_id": self.user_id,
            "username": self.username
        }

class UserData:
    """User data structure"""
    def __init__(self, id: str, username: str, password_hash: str, 
                 created_at: Optional[str] = None, last_login: Optional[str] = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserData':
        """Create UserData from dictionary"""
        return cls(
            id=data["id"],
            username=data["username"],
            password_hash=data["password_hash"],
            created_at=data.get("created_at"),
            last_login=data.get("last_login")
        )
