"""
Simple form-like classes with validation for registration and profile updates.

This lightweight approach avoids external dependencies while keeping validation
logic testable and reusable in `app.py`.
"""
import re
from typing import Tuple, List, Optional

USERNAME_RE = re.compile(r'^[a-zA-Z0-9_-]{3,30}$')
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


class BaseForm:
    """Base form to hold data and provide a common validate signature."""

    def __init__(self, data=None):
        data = data or {}
        # populate attributes from provided mapping, fallback to empty string
        self.username = data.get('username', '').strip()
        self.full_name = data.get('full_name', '').strip()
        self.email = data.get('email', '').strip()
        self.age = data.get('age', '')
        self.about = data.get('about', '').strip()

    def _normalize_age(self) -> Optional[int]:
        """Return age as int if possible, otherwise None for empty."""
        if self.age is None or self.age == '':
            return None
        try:
            return int(self.age)
        except (TypeError, ValueError):
            return None


class RegisterForm(BaseForm):
    """Validator for registration input."""

    def validate(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if not self.username:
            errors.append('Username is required.')
        elif not USERNAME_RE.match(self.username):
            errors.append('Username must be 3-30 chars: letters, numbers, _ or -.')

        if not self.full_name:
            errors.append('Full name is required.')

        if not self.email:
            errors.append('Email is required.')
        elif not EMAIL_RE.match(self.email):
            errors.append('Invalid email address.')

        age_val = self._normalize_age()
        # Accept non-integer ages as 'unset' rather than treating them as an error.
        if age_val is not None:
            if age_val < 0 or age_val > 150:
                errors.append('Age must be between 0 and 150.')
            else:
                self.age = age_val
        else:
            # normalize empty or non-integer ages to None (not an error)
            self.age = None

        if self.about and len(self.about) > 500:
            errors.append('About must be 500 characters or fewer.')

        return (len(errors) == 0, errors)


class UpdateForm(BaseForm):
    """Validator for updating profile (username not changed here)."""

    def validate(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        # username not required for update since it's in URL, but if present validate
        if self.username:
            if not USERNAME_RE.match(self.username):
                errors.append('Username must be 3-30 chars: letters, numbers, _ or -.')

        if not self.full_name:
            errors.append('Full name is required.')

        if not self.email:
            errors.append('Email is required.')
        elif not EMAIL_RE.match(self.email):
            errors.append('Invalid email address.')

        age_val = self._normalize_age()
        # Accept non-integer ages as 'unset' rather than treating them as an error.
        if age_val is not None:
            if age_val < 0 or age_val > 150:
                errors.append('Age must be between 0 and 150.')
            else:
                self.age = age_val
        else:
            # normalize empty or non-integer ages to None (not an error)
            self.age = None

        if self.about and len(self.about) > 500:
            errors.append('About must be 500 characters or fewer.')

        return (len(errors) == 0, errors)
