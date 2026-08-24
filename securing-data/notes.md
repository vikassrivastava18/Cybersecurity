## Passwords 
- Important not to store passwords as plain texts.
- Hashing algorithms with salting do a great job in keeping passwords secure.

## Assignment
<p>Update the code to make registration secure.
Implement hashing algorithms like SHA-256 and then more secured like algorithms like PBKDF2 salting.
Use below code snippet</p>

```
import hashlib
import os
import secrets

def hash_password(password: str) -> tuple[bytes, bytes]:
    """Generates a secure random salt and hashes the password."""
    # 1. Generate a cryptographically secure 16-byte random salt
    salt = os.urandom(16)
    
    # 2. Hash the password using PBKDF2 with SHA-256 and 600,000 iterations
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        600000
    )
    return salt, hashed_password

def verify_password(stored_salt: bytes, stored_hash: bytes, provided_password: str) -> bool:
    """Re-hashes the input password with the stored salt to verify it."""
    # 1. Compute the hash of the login attempt using the original salt
    new_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        provided_password.encode('utf-8'), 
        stored_salt, 
        600000
    )
    
    # 2. Use secrets.compare_digest to prevent timing attacks
    return secrets.compare_digest(stored_hash, new_hash)


# --- Example Usage ---
if __name__ == "__main__":
    raw_password = "SuperSecretPassword123"
    
    # Registration phase: Create and store the salt and hash
    salt, password_hash = hash_password(raw_password)
    print(f"Stored Salt (hex): {salt.hex()}")
    print(f"Stored Hash (hex): {password_hash.hex()}\n")
    
    # Login phase: Testing correct and incorrect passwords
    login_attempt_1 = "SuperSecretPassword123"
    login_attempt_2 = "WrongPassword123"
    
    print(f"Attempt 1 Match: {verify_password(salt, password_hash, login_attempt_1)}") 
    print(f"Attempt 2 Match: {verify_password(salt, password_hash, login_attempt_2)}")
```