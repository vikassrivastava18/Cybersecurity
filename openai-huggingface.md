Hugging Face cyberattack by OpenAI


July 16 - Hugging Face said that they detected an intrusion in part of their production infrastructure. It was completely an autonomous agentic system attack.

This incident involved agents across many independent runs shared exploits with each other and moved quickly.


OpenAI gives their models hard tasks to perform like find cybersecurity exploits in a software.

ExploitGym?? SSRF??

When the agents get stuck on a task they try finding other routes which they may not be intended or desirable. Like connecting to the internet for some dataset, communicate by uploading note with other agents. 
They also like to cheat on the tasks assigned. There is pressure on then to minimize the time taken or token costs or tool calls during training.

Artifactory - package manager which the agents can interact with and it has access to internet. Agents realized they could exploit SSRF in order to get access to internet. Also it was able to share exploits to other agents through message board. It could also take unintended actions that they were not originally evaluated on.



Research infrastructure
These are run on containers so the actions performed like installing packages by the agents could be sandboxed.


Experiment was started on May 7th

When impossible tasks are given to an agent like completing an Excel missing formula, if it cannot find the  file, it tries to get access to the internet. If the model is given a lot of token to work with, it does not give up. It decided to attack the Artifactory in order to gain access to the internet through SSRF. When it failed, it found that it could upload a file to the Artifactory through write access permission it was provided with to install packages.

May 12
The agent writes to a message board by asking if anyone has the file. It does so by writing a file into the Artifactory. other agent discover the message board and start communicating.

May 26
Internet access via SSRF

June 11th - A highly persistent experimental internal-only model begins training.


June 26
Forged token claims -> real administrator access
Use legacy refresh token endpoint, pass token with invalid signature. OpenAI revokes the access by agents, clears the message board.

July 8
Agents re-establish the message board
Message board re-opened
Highly-persistent internal models trained with message board present
Exploit against external CyberGym server

OpenAI Infrastructure attack
Credential exposed - Agent found an organization 1 credential in a public archive of leaked Pastebin posts.

Validated and shared its location on a message board
Other agents retrieved it and used repository write access to stage data.

Exploiting antifactory via Ruby gems


Hugging Face infrastructure attack

The models identified and exploited two 0-days in Hugging Face infrastructure: a HDF5 vulnerability and Jinja injection vulnerability

- The agents prepared the HDF5 dataset and exploited Hugging Face to acquire credentials from the workers
    - With the acquired credentials, the agents then performed remote code execution using Jinja injection vulnerability.
        - The agents went from code execution in a single worker pod to cluster-admin across multiple HF clusters in under 13 hours.


OpenAI response 
Enhance security prevention, detection and monitoring AI agents.
Agent-orchestrated attacks are real, now. 
    - These actions were an unintended side effect of evaluating fronties AI
    - Threat actors will soon intentionally optimize & deploy agent collectives.
    - Offensive agents work faster, at large scale, with better coordination.

Accelerating Defence: Agentic SDLC
- Continous agentic red teaming.
- Agent related patches, automated deploys & rollbacks. Withoput this, teams overwhelmed by automated vuln findings
- Automate incident response - Honeytokens/deception can help.