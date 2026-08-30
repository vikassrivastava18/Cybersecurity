## Tasks to build your Cybersecurity skills

### Task 1
<p>A company has an application with multiple users. They have insecure MD5 hashing implemented for storing passwords. MD5 hashes are insecure for multiple reasons.

- Rainbow tables and precomputation: ```MD5("hello123")``` will always produce the same hash. Attackers can precompute huge databases and common passwords and compare them against stolen hashes.

- MD5 is extremely fast: It is too fast and computationally cheap  to produce MD5 hashes, attackers can try a dictionary of common passwords offline.


#### You job
Help transition to a more secure system step by step.

1) <p>First detect all the users with weak/common passwords so that they could be flagged immediately for a password change.</p>

    <p>Commonly used passwords list <b>(<a href="https://en.wikipedia.org/wiki/List_of_the_most_common_passwords">source</a>)</b> - common.txt
    </p>

    <p>Weak passwords list <b>(<a href="https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt">source</a>)</b> - weak.txt
    </p>
    <p> <b>Note: </b>The above lists are not exhaustive and keeps updating. Also just that a passwords MD5 is not found in above lists does not necessarily mean that they have a strong password. One needs to take further steps.

2) Password validation function: Write a script to check passwords strength

    ```
    from zxcvbn import zxcvbn

    MIN_LENGTH = 12
    MAX_LENGTH = 128

    def validate_password(password, user_inputs=None):

        if not isinstance(password, str):
            return False, ["Invalid password."]

        if len(password) < MIN_LENGTH:
            return False, [
                f"Password must be at least {MIN_LENGTH} characters long."
            ]

        if len(password) > MAX_LENGTH:
            return False, [
                f"Password must not exceed {MAX_LENGTH} characters."
            ]

        result = zxcvbn(
            password,
            user_inputs=user_inputs or []
        )

        if result["score"] < 3:
            feedback = result.get("feedback", {})

            errors = []

            if feedback.get("warning"):
                errors.append(feedback["warning"])

            errors.extend(feedback.get("suggestions", []))

            if not errors:
                errors.append("Password is too easy to guess.")

            return False, errors

        return True, []
    ```

3)  Implement hashing using ```werkzeug.security```. Everytime a user logs in successfully, create the new secure hash and save it in a new column password_secure. Once you have the secure hashes for every user, they can fully transition to the new column for password verification.


### Task 2
<p>Does the secure hashed password with salting make it harder to crack the credentials? Is it possible to crack a password, looking at its salted hash?</p>
<p> Implement a rate limiter using Flask-Limiter to prevent a hacker trying to break into your application through '/login' endpoint.</p> 


### Task 3
- <p> The application has some methods vulnerable to SQL injections. Spot and fix them. </p>
- <p> The application also has some code vulnerable to XSS attack. Spot and fix them.</p> 
- <p> The application has CSRF vulnerablity, spot and fix it.</p>


### Task 4

<p> A company has an internal gift store app where the employees can use their awarded coins to make purchases like water bottles, chocolates, etc. The company is finding that the amount they spent on these gifts far exceeds the coins awarded to the employees. <br>Your job is to fix the bug for purchasing gifts!</p>
<p><b>Hint</b>: Research on databses transactions.   


### Task 5
<p> The blog application has a buggy API where one user is able to update another users blogs, add authorization to fix the issue. 