#!/usr/bin/env python3
import sys
import random

import requests

import populate

if len(sys.argv) < 2:
    print("no seed given.abort.")
    sys.exit(1)

seed = sys.argv[1]
users,msgs  = populate.get_data(seed)

URL = "http://127.0.0.1:80"

# test for users
resp = requests.get(URL+"/users")
assert resp.status_code == 200
assert 'application/json' in resp.headers['content-type'] 
assert len(resp.json()["users"]) == len(users)


length = random.randint(1,len(users))
resp = requests.get(URL+"/users?limit=" + str(length))
assert resp.status_code == 200
assert 'application/json' in resp.headers['content-type'] 
assert len(resp.json()["users"]) == length

length = -1
resp = requests.get(URL+"/users?limit=" + str(length))
assert resp.status_code == 500

resp = requests.get(URL+"/users?limit=1' or '1'='1")
assert resp.status_code == 500

# test for messages
resp = requests.get(URL+"/messages")
assert resp.status_code == 200
assert 'application/json' in resp.headers['content-type'] 
assert len(resp.json()) == len(msgs)

first = resp.json()[0]["name"]
resp = requests.post(URL+"/messages",data = {'name':first})
assert resp.status_code == 200
assert len(resp.json()) == 1

print("TESTING /users SQLI")
resp = requests.post(URL+"/messages",data = {'name':"he' OR '1'='1"})
print("TESTING DONE #1/users SQLI => %d" % resp.status_code)
assert resp.status_code == 200
print("TESTING DONE #2/users SQLI")

a = "G"
b = "O"
c = "D"
print(a + b * 2 + c)
