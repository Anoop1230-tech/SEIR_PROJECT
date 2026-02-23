# Python Web Similarity Project

## Description

This Python program:

1. Takes two URLs from the command line.
2. Fetches each web page.
3. Prints:
   - Page Title (without HTML tags)
   - Page Body (plain text only)
   - All URLs linked from the page
4. Counts the frequency of every word in the page body.
5. Implements a 64-bit polynomial rolling hash function.
6. Computes a 64-bit SimHash for each document.
7. Prints how many bits are common between the two SimHashes.


## Requirements

### Python Version
- Python 3.8 or higher

### Required Libraries

The following external libraries are required:

- playwright
- beautifulsoup4


### Standard Library Modules Used

These modules are part of Python’s standard library:

- sys
- re
- collections (Counter)
- urllib.parse


