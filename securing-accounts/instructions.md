## Fix the accounts security

### Task 1
<p>A company has an application with multiple users. They have MD5 hashing implemented for storing passwords. They want to know and inform users whose password is insecure. Write a script to detect the weak and commonly used passwords from the database. </p>
<b>Commonly used passwords list</b> (common.txt) - https://en.wikipedia.org/wiki/List_of_the_most_common_passwords</p>
<b>Weak passwords list</b> (weak.txt) - https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt


### Task 2
<p>To make the application more secure add these two functionalities</p>

- Password validation function to check for these
    - Minimum password length should be 8.
    - Password must has at least one uppercase char, on lowercase char, one number and one special char. 
- Implement hashing with salting using 


### Task 3
<p> Find the time it might take for a hacker to crack a database passwords with modern security implemented. </p>
<p>Does the hashed password with salting make it harder to crack the credentials?</p>
