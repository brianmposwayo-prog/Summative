"""
JSON-backed DB helper for user profiles.

Provides simple read/write helpers that store a list of user dicts in `users.json`.
This module keeps file operations small and documented for clarity.
"""
import json
import os
from typing import List, Optional, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.json')


def _ensure_db_exists():
    """Create the DB file with an empty list if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)


def _read_db() -> List[Dict]:
    """Return the list of users from the JSON file."""
    _ensure_db_exists()
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_db(users: List[Dict]):
    """Overwrite the JSON file with the provided list of users."""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)


def get_all_users() -> List[Dict]:
    """Return all user records."""
    return _read_db()


def get_user(username: str) -> Optional[Dict]:
    """Return a single user by username or None if not found."""
    users = _read_db()
    for u in users:
        if u.get('username') == username:
            return u
    return None


def add_user(user: Dict):
    """Add a new user to the DB. Caller should ensure uniqueness."""
    users = _read_db()
    # Prevent duplicate usernames: if username exists, do not add.
    username = user.get('username')
    if username and any(u.get('username') == username for u in users):
        return False
    users.append(user)
    _write_db(users)
    return True


def update_user(username: str, updated: Dict) -> bool:
    """Update an existing user. Returns True if updated, False if not found."""
    users = _read_db()
    for i, u in enumerate(users):
        if u.get('username') == username:
            users[i] = updated
            _write_db(users)
            return True
    # If not found, create the user record (create-on-update behaviour).
    users.append(updated)
    _write_db(users)
    return True
