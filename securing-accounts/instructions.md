## Accounts security

### Task 1
<p>A company has an application with multiple users. They have MD5 hashing implemented for storing passwords. They want to know and inform users whose password is insecure. Write a script to detect the weak and commonly used passwords from the database. </p>
<p>Commonly used passwords list <b>(<a href="https://en.wikipedia.org/wiki/List_of_the_most_common_passwords">source</a>)</b> - common.txt
    
</p>

<p>Weak passwords list <b>(<a href="https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt">source</a>)</b> - weak.txt
</p>

### Task 2
<p>To make the application more secure add these two functionalities</p>

- Password validation function to check for these
    - Minimum password length should be 8.
    - Password must has at least one uppercase char, on lowercase char, one number and one special char. 
- Implement hashing with salting.


### Task 3
<p>Does the hashed password with salting make it harder to crack the credentials? Is it possible to guess a password, looking at its salted hash?</p>
<p> If a hacker still tries to hack users account, what steps can help prevent this?</p> 

