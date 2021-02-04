# Wayback

# Dependencies:
* Python 3.5+
* pip install urllib
* pip install requests
* pip install json
* pip install datetime
* pip install sys
* pip install time

---

## archive.py

A basic and quick archiving tool for the Internet Archive.

### Usage:

There are two ways to use this:

- python archive.py "www.google.ca"
- python archive.py -f "links.txt"

where 'links.txt' is a file located in your current working directory, with a new link on each line.

### Notes:
Uses the Wayback Availability API.

A link gets 3 tries to archive properly. If it doesn't archive, then it gets put in a log file. You can re-run the script on this log file to try and archive what you couldn't before.

About 40 links get checked at a time and then a 4 minute wait is done to prevent the TooMany Redirects error.
 