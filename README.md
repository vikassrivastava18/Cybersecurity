## Tasks to build your Cybersecurity skills

### Task 1

A company has an application with multiple users. They have insecure MD5 hashing implemented for storing passwords. MD5 hashes are insecure for multiple reasons.

- Rainbow tables and precomputation: MD5("hello123") will always produce the same hash. Attackers can precompute huge databases of common passwords and compare them against stolen hashes.
- MD5 is extremely fast: it is computationally cheap to produce MD5 hashes, so attackers can try a dictionary of common passwords offline.

Your job is to help transition to a more secure system step by step.

1. Detect all users with possible weak or common passwords so they can be flagged immediately for a password change.

   Use the commonly used passwords list: source - common.txt

   Use the weak passwords list: source - weak.txt

   Note: These lists are not exhaustive and keep changing. Also, the fact that a password’s MD5 hash is not found in the list does not necessarily mean the password is strong. More steps are needed.

2. Write a password validation function to check password strength. Use the zxcvbn package from Dropbox to detect password strength.

   Install it with:
   pip install zxcvbn

3. Implement hashing using werkzeug.security. Once secure hashes are created for every user, they can fully transition to the new column for password verification.

### Task 2

Does a securely hashed password with salting make it harder to crack credentials? Is it possible to crack a password by looking at its salted hash?

Implement a rate limiter using Flask-Limiter to prevent a hacker from trying to break into your application through the /login endpoint.

### Task 3

- The application has some methods vulnerable to SQL injection. Spot and fix them.
- The application also has code vulnerable to XSS attacks. Spot and fix them.
- The application has a CSRF vulnerability. Spot and fix it.

### Task 4

A company has an internal gift store app where employees can use awarded coins to make purchases such as water bottles, chocolates, and other items. The company has found that the amount spent on gifts far exceeds the coins awarded to employees.

Your job is to fix the bug for purchasing gifts.

Hint: Research database concurrency.

### Task 5

The blog application has a buggy API where a user can update another user’s blog. Add authorization to fix the issue.



