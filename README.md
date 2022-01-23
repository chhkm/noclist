# noclist
## Background
This program retrieves the NOC list from the BADSEC server and prints the list as a JSON. If any call to the server fails three times, the program will exit with a non-zero status code.  
Refer to Ad Hoc's Noclist homework for more information --> https://homework.adhoc.team/noclist/  

---

## Set Up
### Prerequisite
* BADSEC server running on port 8888
* Python 3.6+

*Note, be in the root of this repo before you begin!

### Create a virtual environment
`$ python3 -m venv noclist`

### Activate virtual environment
`$ source noclist/bin/activate`

### Install dependencies
`$ python3 -m pip install -r requirements.txt`

---

## Run program
`$ python3 noclist.py`

---

## Run unit tests
`$ python3 -m unittest`

---

## Deactivate virtual environment
`$ deactivate noclist`
