## Notes

A DDoS attack stands for Distributed Denial of Service attack. The goal is to make a service such as a website or server unavailable to its intended users by overwhelming it with traffic or requests.

The “distributed” part means the attack comes from many different sources at once, often thousands of compromised computers or devices known as a botnet. This makes the attack more powerful and harder to stop because blocking one source is not enough.

A simple analogy is a small shop that can serve only one customer at a time. If hundreds of fake customers crowd the doorway all at once, real customers cannot get in. That is essentially what a DDoS attack does to a server.

DDoS attacks are commonly defended against using:
- Rate limiting: restricting how many requests a single source can make in a period of time.
- Firewalls and filtering: blocking suspicious traffic based on patterns or known bad sources.
- Load balancing: spreading traffic across multiple servers so no single server becomes overwhelmed.
- Content Delivery Networks (CDNs): absorbing and distributing large amounts of traffic across many servers worldwide.

This connects to networking concepts such as TCP/IP, where data is sent in packets between clients and servers. A DDoS attack abuses the normal request-response model by sending far more requests than a server can handle. Understanding IP addresses helps explain why “distributed” matters: blocking one IP is easy, but blocking thousands is difficult.

SETI@Home was a distributed computing project run by the University of California, Berkeley, from 1999 to 2020. Its goal was to search for extraterrestrial intelligence by analyzing radio signals from space and looking for patterns that might indicate intelligent life.

It worked by splitting enormous amounts of radio data into smaller chunks and distributing them to volunteers’ personal computers around the world. When a computer was idle, such as during a screensaver, it would download a chunk, analyze it, and send the results back.

This is interesting in computer science because it is a classic example of distributed computing: many ordinary machines work together to solve a huge problem. It later inspired BOINC (Berkeley Open Infrastructure for Network Computing), a platform used for many volunteer computing projects.

A malware attack is possible in such a system because distributed computing involves running software on many machines. However, projects like SETI@Home and BOINC were designed with safeguards. The software ran in a sandboxed environment, limiting what it could access on the user’s computer. Data chunks were processed and results returned, and the software did not execute arbitrary code from unknown sources. Users also installed trusted software from a verified source.

That said, any system that distributes and runs code across many machines is a potential attack surface if not properly secured. This is exactly why sandboxing, verification, and trusted sources matter so much in cybersecurity.

Sandboxing is a security technique where a program runs in an isolated, restricted environment separate from the rest of the system. The sandbox acts like a walled-off playground. Code may run and do its work inside, but it cannot reach out and interfere with things outside. If the code is malicious or buggy, the damage is contained.

Sandboxing typically restricts:
- Access to the file system
- Access to the network
- Access to other programs or system resources

Real-world examples include web browsers sandboxing each tab so a malicious website cannot take over an entire computer, and mobile apps running in sandboxes that require user permission for camera or contact access. In this context, SETI@Home’s analysis code could process data without snooping through a user’s personal files.

Once an adversary discovers an open port through scanning, they may:
1. Identify the service running on that port, such as HTTP on port 80 or SSH on port 22.
2. Determine the service version to look for known vulnerabilities.
3. Attempt exploitation using methods such as brute-forcing credentials, exploiting a known vulnerability, or sending malicious input to crash or manipulate the service.
4. Establish a foothold and potentially install malware or move deeper into the network.

This is why keeping software updated, closing unused ports, and using firewalls are essential defenses. Every open port can be a potential entry point.

A zero-day attack exploits a vulnerability that is unknown to the software vendor. This means there have been zero days to create a patch. Notable examples include:
- Stuxnet (2010): a worm that targeted industrial control systems, specifically Iranian nuclear centrifuges.
- Heartbleed (2014): a serious bug in OpenSSL that allowed attackers to read sensitive memory from servers.
- Aurora (2009): an attack that exploited a zero-day vulnerability in Internet Explorer to target several large companies, including Google.
- Sony Pictures Hack (2014): malware that used previously unknown exploits to breach and damage Sony’s systems.

Zero-day attacks are dangerous because there is no existing patch or fix when the attack begins. Defenders are effectively caught off guard, and the vulnerabilities are often highly valued and sold on black markets.

Security through obscurity is the idea of relying on the secrecy of a design or implementation as the main method of protection rather than on strong, proven security measures. The core problem is that if the only thing protecting a system is the fact that attackers do not know how it works, then security collapses the moment that secret is discovered.

Examples include:
- Hiding a house key under the doormat: this is not real security, just concealment.
- Renaming an SSH port from the default 22 to 2222: this may reduce automated scans, but a determined attacker can still find it.
- Hardcoding a “secret” URL such as example.com/admin_hidden_page with no actual authentication: anyone who discovers or guesses it gains access.

The key takeaway is that obscurity can be a minor extra layer, but it should never be the primary defense. Good security should hold even when an attacker knows exactly how the system works. This principle is known as Kerckhoffs’s principle.

Penetration testing, or pen testing, is an authorized, simulated cyberattack on a system used to find and fix vulnerabilities before real attackers can exploit them. Ethical hackers, or “white hats,” deliberately attempt to break into a system using the same tools and techniques as malicious attackers, but with permission and with the goal of improving security.

Typical steps include:
- Reconnaissance: gathering information about the target
- Scanning: identifying open ports, services, and weaknesses
- Exploitation: attempting to break into the system using discovered weaknesses
- Reporting: documenting findings and recommending fixes

Pen testing is a proactive defense. Instead of waiting to hope a system is secure, security teams actively test it to discover gaps and fix them before real attacks occur.

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