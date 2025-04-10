# gtfobinsearch
Search engine for possible privilege escalation in Linux systems using the website https://gtfobins.github.io

Usage:
`python3 gtfobinsearch.py -b [binary or text file] -m [permission or leave empty for all permissions] -v`

    The -b argument accepts either the name of a binary (e.g., bash) or a .txt file containing a list of binary names.

    The -m argument specifies the type of privilege you want to check. If left empty, it will show all the available permissions for that binary.

    The -v argument requests the description and instructions for privilege escalation using the specified binary and permission.
