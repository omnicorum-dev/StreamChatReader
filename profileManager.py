import os
import random

language_names = ["en-AU-Polyglot-1",
         "en-AU-Standard-B",
         "en-AU-Standard-C",
         "en-AU-Standard-D",
         "en-IN-Standard-A",
         "en-IN-Standard-B",
         "en-IN-Standard-C",
         "en-IN-Standard-D",
         "en-GB-Standard-A",
         "en-GB-Standard-B",
         "en-GB-Standard-C",
         "en-GB-Standard-D",
         "en-GB-Standard-F",
         "en-US-Journey-D",
         "en-US-Journey-F",
         "en-US-Polyglot-1",
         "en-US-Standard-A",
         "en-US-Standard-B",
         "en-US-Standard-C",
         "en-US-Standard-D",
         "en-US-Standard-E",
         "en-US-Standard-F",
         "en-US-Standard-G",
         "en-US-Standard-H",
         "en-US-Standard-I",
         "en-US-Standard-J"]
language_codes = ["en-AU",
                  "en-AU",
                  "en-AU",
                  "en-AU",
                  "en-AU",
                  "en-IN",
                  "en-IN",
                  "en-IN",
                  "en-IN",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-GB",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US",
                  "en-US"]

def check_profile(username):
    profiles = open("profiles.txt", 'r')
    
    file = profiles.read()
    
    if username in file:
        profiles.close()
        return True
    else:
        profiles.close()
        return False
    
def create_profile(username):
    langNum = random.randint(0, 25)
    profiles = open("profiles.txt", 'a')
    lang_code = language_codes[langNum]
    lang_name = language_names[langNum]
    profiles.write("\n" + username + "@" + lang_code + "@" + lang_name)
    print("new profile created")
    return [username, lang_code, lang_name]
    profiles.close()
    
def get_profile(username):
    profiles = open("profiles.txt", 'r')
    
    line = profiles.readline()
    while line != '':
        print("parse")
        if username in line:
            print(line)
            elements = line.split("@")
            return elements
        else:
            line = profiles.readline()
    return ['', '', '']

def profiler(username):
    profiles = open("profiles.txt", 'r')
    
    has_profile = False
    
    line = profiles.readline()
    while line != '':
        if username in line:
            # profile already exists
            has_profile = True
            print(line)
            elements = line.split("@")
            print(elements[0])
            print(elements[1])
            print(elements[2])
        line = profiles.readline()
    
    # print(has_profile)
    
    if not has_profile:
        langNum = random.randint(0, 25)
        profiles.close()
        profiles = open("profiles.txt", "a")
        profiles.write("\n" + username + "@" + language_codes[langNum] + "@" + language_names[langNum])
        print("new profile created")
        
    profiles.close()

print(check_profile("omnicorum"))
print(get_profile("omnicorum"))
