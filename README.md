# gtfobinsearch
Search engine for a possible privilege escalation in Linux systems using the web https://gtfobins.github.io

Use:
`python3 gtfobinsearch.py -b [bin or text file] -m [permission or empty for all permissions] -v' 

In the -b argument, we can parse the name of a bin, for example, bash, or a txt file to prove a list of names.

In the -m argument, we can parse the type of privilege that we want to check. If we let it empty, it show all the permissions that we could use with that bin.

With the -v, argument, we are asking to the script for the description and instructions of the privilege escalation with that bin and permission.
