### SQL Injection
An adversary may attempt to trick SQL into executing malicious code.

>> SELECT * FROM users
>> WHERE username = '{username}';

With above SQL code, an adversary may insert following code:
>> malan'; DELETE FROM users; --

Results in:
>> SELCECT * FROM users
>> WHERE username = 'malan'; DELETE FROM users; --'


Another example
>> SELECT * FROM users
>> WHERE username = '{username}' AND password = '{password}';

An adversary may insert code like nelow in password field:
>> ' OR '1'='1

Which becomes:
>> SELECT * FROM users
>> WHERE (username = 'malan' and password = '') OR '1'='1';
Resulting in returning all the users in the database


### Prepared Statement
Pre-designed snippets of code that correctly handle many database functions, including user input.

Such statements ensure that user-inputted data is properly escaped.

A prepared statement will take code as the following...
>> SELECT * FROM users
>> WHERE username = '{username}'

and replace it with:
>> SELECT * FROM users
>> WHERE username = ?

Prepared statements will look for any ' characters and replace them with ''. Hence, our previous attack would be rendered as:
>> SELECt * FROM users
>> WHERE username = 'malan''; DELETE FROM users; --'
' at the end of 'malan' is replaced with '', rendering the malicious code inoperable.