## Tasks to build your Cybersecurity skills

### Task 1
<p>A company has an application with multiple users. They have insecure MD5 hashing implemented for storing passwords. They want to know and inform users whose password is weak/common before it is hacked. Write a script to detect the weak and commonly used passwords from the database.</p>
<p>Commonly used passwords list <b>(<a href="https://en.wikipedia.org/wiki/List_of_the_most_common_passwords">source</a>)</b> - common.txt
</p>


<p>Weak passwords list <b>(<a href="https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt">source</a>)</b> - weak.txt
</p>

### Task 2
<p>To make the application more secure add these two functionalities:</p>

- Password validation function to check for these
    - Minimum password length should be 8.
    - Password must has at least one uppercase char, on lowercase char, one number and one special char. 
- Implement hashing with salting before saving passwords.


### Task 3
<p>Does the hashed password with salting make it harder to crack the credentials? Is it possible to crack a password, looking at its salted hash?</p>
<p> Implement a rate limiter using Flask-Limiter to prevent a hacker trying to break into your application through '/login' endpoint.</p> 


### Task 4
- <p> The application has some methods vulnerable to SQL injections. Spot and fix them. </p>
- <p> The application also has some code vulnerable to XSS attack. Spot and fix them.</p> 
- <p> The application has CSRF vulnerablity, spot and fix it.</p>


### Task 5

<p> A company has an internal gift store app where the employees can use their awarded coins to make purchases like water bottles, chocolates, etc. The company is finding that the amount they spent on these gifts far exceeds the coins awarded to the employees. <br>Your job is to fix the bug for purchasing gifts!</p>
<p><b>Hint</b>: Research on databses transactions.   