from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys, os, base64, subprocess, random, sqlite3, string


import sys, time
import sqlite3
import base64

PASSWORDS = [
        "123456",
        "123456789",
        "qwerty",
        "password",
        "1234567",
        "12345678",
        "12345",
        "iloveyou",
        "111111",
        "123123",
        "abc123",
        "qwerty123",
        "1q2w3e4r",
        "admin",
        "qwertyuiop",
        "654321",
        "555555",
        "lovely",
        "7777777",
        "welcome",
        "888888",
        "princess",
        "dragon",
        "password1",
        "123qwe"]

ALPHABET = ["", "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def read_user_hashes():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    user_hashes = []

    for row in cursor.execute("SELECT * FROM auth_user"):
        user_hashes.append((row[4], row[1]))

    return user_hashes

def check_list():
    user_hashes = read_user_hashes()

    for user, hash in user_hashes:
        algo, iterations, salt, hash = hash.split("$")
        algo = algo.strip()
        iterations = iterations.strip()
        salt = salt.strip()
        hash = hash.strip()
        hashbytes = base64.b64decode(hash)

        # print("{},{},{},{}".format(algo, iterations, salt, hash))

        for commonpw in PASSWORDS:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=len(hashbytes),
                salt=salt.encode(),
                iterations=int(iterations),
            )
            key_hash = kdf.derive(commonpw.encode())
            # print("{}, {}".format(len(hashbytes), len(key_hash)))
            if (hashbytes == key_hash):
                print("{},{}".format(user, commonpw))
                break

def bruteforce_single(pw):
    # print(pw)
    # print(pw.split("$"))
    algo, iterations, salt, hash = pw.split("$")
    algo = algo.strip()
    iterations = iterations.strip()
    salt = salt.strip()
    hash = hash.strip()
    hashbytes = base64.b64decode(hash)

    if int(iterations) != 1:
        print("Cannot brute-force password in time.")
    else:
        for first in ALPHABET:
            for second in ALPHABET:
                for third in ALPHABET:
                    for fourth in ALPHABET:
                        brute = "{}{}{}{}".format(first, second, third, fourth)
                        # print(brute)
                        kdf = PBKDF2HMAC(
                            algorithm=hashes.SHA256(),
                            length=len(hashbytes),
                            salt=salt.encode(),
                            iterations=int(iterations),
                        )
                        key_hash = kdf.derive(brute.encode())
                        if (hashbytes == key_hash):
                            print("Password cracked: '{}'".format(brute))
                            exit()

        print('Password not cracked.')

if __name__=="__main__":
    if len(sys.argv) == 1:
        check_list()
    elif len(sys.argv) == 2:
        bruteforce_single(sys.argv[1])
