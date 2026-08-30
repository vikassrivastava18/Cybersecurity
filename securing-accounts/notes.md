## Securing accounts
- Adding some strong password validation, like minimum characters length help in securing an account.
- Password hashing with salting is a must for modern applications security

```
import re

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]';`~]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is valid."
```

<p>Frameworks like Django help a lot by providing such features out of the box. In Flask or FastAPI, one needs to install third party packages.</p>

