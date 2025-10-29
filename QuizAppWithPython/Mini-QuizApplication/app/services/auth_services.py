# services/auth_service.py
from app.databases.collections import USERS
from bson import ObjectId
import hashlib
from typing import Optional, Dict, Any


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, password: str, role: str, profile: Optional[Dict[str, Any]] = None):
    """
    Register a user in the USERS collection.

    profile: optional dict with additional profile fields (fullname, dob, address, etc.)
    Returns (success: bool, message: str)
    """
    if USERS.find_one({"username": username}):
        return False, "Username already exists"

    user = {
        "username": username,
        "password": hash_password(password),
        "role": role,  # 'student' hoặc 'teacher'
    }

    if profile:
        # merge profile fields into user doc, avoid overwriting username/password/role
        for k, v in profile.items():
            if k in ("username", "password", "role"):
                continue
            user[k] = v

    USERS.insert_one(user)
    return True, "Registration successful"


def login_user(username: str, password: str):
    """
    Verify username/password. Returns (True, user_dict) on success, otherwise (False, message).
    """
    hashed = hash_password(password)
    user = USERS.find_one({"username": username, "password": hashed})

    if user:
        return True, {"_id": str(user["_id"]), "username": user["username"], "role": user.get("role")}
    else:
        return False, "Invalid username or password"


def change_password(user_id: str, old_password: str, new_password: str):
    """
    Changes the password for a given user.
    Returns (success: bool, message: str)
    """
    try:
        uid = ObjectId(user_id)
    except Exception:
        return False, "Invalid user ID format"

    user = USERS.find_one({"_id": uid})

    if not user:
        return False, "User not found"

    # Verify old password
    if user.get("password") != hash_password(old_password):
        return False, "Incorrect old password"

    # Update with new password
    new_hashed_password = hash_password(new_password)
    USERS.update_one({"_id": uid}, {"$set": {"password": new_hashed_password}})

    return True, "Password updated successfully"
