#!/usr/bin/python3

import re

list_of_emails = set()

my_str = open("/home/kali/Downloads/blob.txt",'r')
output = open("/home/kali/Downloads/list_of_emails.txt",'w')

for line in my_str.readlines():
    line = line.strip('\n')
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)
    for mail in emails:
        list_of_emails.add(mail.lower())


for mail in sorted(list_of_emails):
    output.write(mail+"\n")
    print(mail)
