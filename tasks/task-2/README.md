### How salting works?

The salt is often embedded in the password hash itself. The salt is used to verify a user's credential.

Argon2 and bcrypt store following information together:

- Algorithm identifier (bcrypt/Argon2). Imagine you registered a user when the application was using bcrypt. A year later, you migrate to Argon2, saving the identifier will help not break the appication. 
- Cost/work factor: How computationally expensive the password hashing operation should be.
- Salt
- Password hash

