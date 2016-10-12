import fileinput
import hashlib

def hashfunc(password, salt):
    return hashlib.sha256("potplantpwdb" + password + salt).hexdigest()[0:32]

def test_mutations(password, salt, password_hash):
    if hashfunc(password, salt) == password_hash:
        return password
    if hashfunc(password + "!", salt) == password_hash:
        return test_pass + "!"

    for i in range(0, len(password)):
        test_pass = None
        if(password[i].islower()):
            test_pass = password[0:i] + password[i].upper() + password[i+1:32]
        else:
            test_pass = password[0:i] + password[i].lower() + password[i+1:32]
        if hashfunc(test_pass, salt) == password_hash:
            return test_pass

    for i in range(0, len(password)):
        test_pass = None
        test_pass = password[0:i] + password[i+1:32]
        if hashfunc(test_pass, salt) == password_hash:
            return test_pass

    for i in range(0, len(password)):
        test_pass = None
        test_pass = password[0:i] + password[i] + password[i:32]
        if hashfunc(test_pass, salt) == password_hash:
            return test_pass

    for i in range(0, 10):
        test_pass = password + str(i)
        if hashfunc(test_pass, salt) == password_hash:
            return test_pass

    for i in range(0, 10):
        test_pass = str(i) + password
        if hashfunc(test_pass, salt) == password_hash:
            return test_pass

    if hashfunc(password[::-1], salt) == password_hash:
        return password[::-1]
    if hashfunc(password.replace("a", "@").replace("s", "$"), salt) == password_hash:
        return password.replace("a", "@").replace("s", "$") 
    if hashfunc(password + "123", salt) == password_hash:
        return password + "123" 
    if hashfunc(password + "007", salt) == password_hash:
        return password + "007"

users = {}
for line in fileinput.input('users'):
    user, salt = line.replace("\n", "").split(" ")
    users[salt] = user

hashes = {}
for line in fileinput.input('hashes'):
    salt, password_hash = line.replace("\n", "").split(" ")
    hashes[salt] = password_hash


for line in fileinput.input():
    password = line.replace("\n", "")
    for salt, password_hash in hashes.items():
        result = test_mutations(password, salt, password_hash)
        if result != None:
            print("Found " + users[salt] + " : " + result)
