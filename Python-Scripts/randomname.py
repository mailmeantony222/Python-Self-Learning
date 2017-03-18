import string
import random
character = string.lowercase + string.uppercase + string.digits + string.punctuation
char_len = len(character)
# you can specify your password length here
pass_len = random.randint(10,20)
password = ''
for x in range(pass_len):
    password = password + character[random.randint(0,char_len-1)]
print password