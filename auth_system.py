"""
Group F - Authentication Module
Purpose: Authenticate users (librarians/members).
Responsibilities: Basic login system.
"""

import hashlib
from datetime import datetime, timedelta

class AuthSystem:
    """
    Authentication system for the library management system.
    
    Attributes:
        users (dict): Dictionary of users with username as key
        sessions (dict): Dictionary of active sessions
        session_timeout (int): Session timeout in minutes
    """
    
    def __init__(self, session_timeout=30):
        """
        Initialize the authentication system.
        
        Args:
            session_timeout (int): Session timeout in minutes
        """
        self.users = {}
        self.sessions = {}
        self.session_timeout = session_timeout
        self._setup_default_users()
    
    def _setup_default_users(self):
        """
        Set up default users (librarian and sample member).
        """
        # Default librarian account
        self.add_user("librarian", "admin123", "librarian", {
            'name': 'System Librarian',
            'email': 'librarian@library.com'
        })
        
        # Default member account
        self.add_user("member", "member123", "member", {
            'name': 'Sample Member',
            'email': 'member@example.com'
        })
    
    def _hash_password(self, password):
        """
        Hash a password using SHA-256.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_user(self, username, password, role, user_info=None):
        """
        Add a new user to the system.
        
        Args:
            username (str): Username
            password (str): Plain text password
            role (str): User role ("librarian" or "member")
            user_info (dict, optional): Additional user information
            
        Returns:
            bool: True if user was added successfully, False if username exists
        """
        if username in self.users:
            return False
        
        self.users[username] = {
            'password': self._hash_password(password),
            'role': role,
            'info': user_info or {},
            'created_at': datetime.now(),
            'last_login': None
        }
        return True
    
    def authenticate(self, username, password):
        """
        Authenticate a user with username and password.
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            tuple: (success: bool, user_data: dict or error_message: str)
        """
        if username not in self.users:
            return False, "Username not found"
        
        user = self.users[username]
        if user['password'] != self._hash_password(password):
            return False, "Invalid password"
        
        # Update last login
        user['last_login'] = datetime.now()
        
        return True, {
            'username': username,
            'role': user['role'],
            'info': user['info']
        }
    
    def create_session(self, username):
        """
        Create a new session for a user.
        
        Args:
            username (str): Username
            
        Returns:
            str: Session token
        """
        import uuid
        
        session_token = str(uuid.uuid4())
        expiry_time = datetime.now() + timedelta(minutes=self.session_timeout)
        
        self.sessions[session_token] = {
            'username': username,
            'created_at': datetime.now(),
            'expires_at': expiry_time
        }
        
        return session_token
    
    def validate_session(self, session_token):
        """
        Validate a session token.
        
        Args:
            session_token (str): Session token to validate
            
        Returns:
            tuple: (valid: bool, username: str or None)
        """
        if session_token not in self.sessions:
            return False, None
        
        session = self.sessions[session_token]
        
        # Check if session has expired
        if datetime.now() > session['expires_at']:
            del self.sessions[session_token]
            return False, None
        
        return True, session['username']
    
    def logout(self, session_token):
        """
        Logout a user by invalidating their session.
        
        Args:
            session_token (str): Session token to invalidate
            
        Returns:
            bool: True if session was found and invalidated
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
    
    def change_password(self, username, old_password, new_password):
        """
        Change a user's password.
        
        Args:
            username (str): Username
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Verify current password
        auth_success, _ = self.authenticate(username, old_password)
        if not auth_success:
            return False, "Current password is incorrect"
        
        # Update password
        self.users[username]['password'] = self._hash_password(new_password)
        return True, "Password changed successfully"
    
    def get_user_role(self, username):
        """
        Get the role of a user.
        
        Args:
            username (str): Username
            
        Returns:
            str or None: User role if user exists, None otherwise
        """
        if username in self.users:
            return self.users[username]['role']
        return None
    
    def is_librarian(self, username):
        """
        Check if a user is a librarian.
        
        Args:
            username (str): Username
            
        Returns:
            bool: True if user is a librarian
        """
        return self.get_user_role(username) == 'librarian'
    
    def is_member(self, username):
        """
        Check if a user is a member.
        
        Args:
            username (str): Username
            
        Returns:
            bool: True if user is a member
        """
        return self.get_user_role(username) == 'member'
    
    def cleanup_expired_sessions(self):
        """
        Remove all expired sessions.
        
        Returns:
            int: Number of sessions removed
        """
        current_time = datetime.now()
        expired_sessions = [
            token for token, session in self.sessions.items()
            if current_time > session['expires_at']
        ]
        
        for token in expired_sessions:
            del self.sessions[token]
        
        return len(expired_sessions)
    
    def get_active_sessions(self):
        """
        Get information about all active sessions.
        
        Returns:
            list: List of active session information
        """
        current_time = datetime.now()
        active_sessions = []
        
        for token, session in self.sessions.items():
            if current_time <= session['expires_at']:
                active_sessions.append({
                    'username': session['username'],
                    'created_at': session['created_at'],
                    'expires_at': session['expires_at']
                })
        
        return active_sessions

# Simple authentication functions for backwards compatibility
def authenticate(username, password, user_db=None):
    """
    Simple authentication function (deprecated - use AuthSystem class).
    
    Args:
        username (str): Username
        password (str): Password
        user_db (dict): User database (deprecated)
        
    Returns:
        bool: True if authentication successful
    """
    # This is a simplified version for backwards compatibility
    default_users = {
        'librarian': 'admin123',
        'member': 'member123'
    }
    
    if user_db:
        return user_db.get(username) == password
    else:
        return default_users.get(username) == password